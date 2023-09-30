# xer-reader
# reader.py

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import BinaryIO

from xer_reader.src.table_info import TableInfo

REQUIRED_TABLES = {"CALENDAR", "CURRTYPE", "PROJECT", "PROJWBS"}
date_format = "%Y-%m-%d"


class XerReader:
    """Open a XER file exported from Primavera P6 and read its contents."""

    CODEC = "cp1252"
    file_name: str
    data: str

    def __init__(self, file: str | Path | BinaryIO) -> None:
        self.file_name, self.data = _read_file(file)

        _file_info = _parse_file_info(self.data)
        self.export_version: str = _file_info[0]
        self.export_date: datetime = datetime.strptime(_file_info[1], date_format)
        self.export_user: str = _file_info[4]
        self.tables: dict[str, dict[int, dict[str, str]]] = {
            name: rows
            for table in self.data.split("%T\t")[1:]
            for name, rows in _parse_table(table).items()
        }

    def check_errors(self) -> list[str]:
        """Check XER file for missing tables and orphan data

        Returns:
            list[str]: Descriptions of missing information
        """
        errors = set()

        id_map = {
            table.value["key"]: table.name for table in TableInfo if table.value["key"]
        }

        # Check for minimum tables required to be in the XER
        for name in REQUIRED_TABLES:
            if name not in self.tables:
                errors.add(f"Missing Required Table {name}")

        # Check for required table pairs
        for table, data in self.tables.items():
            table_info = TableInfo[table].value
            for t in table_info["depends"]:
                if t not in self.tables:
                    errors.add(f"Missing Table {t} Required for Table {table}")

            for row in data.values():
                for key, val in row.items():
                    if val == "":
                        continue
                    if not key.endswith("_id"):
                        continue
                    if key == "parent_wbs_id" and row["proj_node_flag"] == "Y":
                        continue
                    clean_key = key if key in id_map else _clean_id_label(key)
                    if clean_key:
                        if val not in self.tables.get(id_map[clean_key], {}):
                            errors.add(f"Orphan data {key} [{val}] in table {table}")

        return list(errors)

    def delete_tables(self, *table_names: str) -> str:
        """
        Delete tables from XER file.
        Does not modify `XerReader.data` attribute, but returns a new string.

        Args:
            *table_names (str): table names to remove from XER file

        Returns:
            str: XER File String with tables removed
        """
        if not table_names:
            raise ValueError("Must pass at least one table name")

        rev_data = self.data
        for name in table_names:
            table_search = re.compile(rf"%T\t{name.upper()}\n(.|\s)*?(?=%T|%E)")
            rev_data = table_search.sub("", rev_data)
        return rev_data

    def get_table_str(self, table_name: str) -> str:
        """Get string for a specific table in the XER file.

        Args:
            table_name (str): Name of table

        Returns:
            str: Table header and rows
        """
        re_search = re.compile(rf"(?<=%T\t{table_name.upper()}\n)(.|\s)*?(?=%T|%E)")
        if found_table := re_search.search(self.data):
            return re.sub(r"%[TFR]\t", "", found_table.group())
        return ""

    def to_csv(self, file_directory: str | Path = Path.cwd()) -> None:
        """
        Generate a CSV file for each table in the XER file.
        Uses `tab` as the delimiter.

        Args:
            file_directory (str | Path, optional): Directory to save CSV files.
            Defaults to current working directory.
        """
        for name, table in self.tables.items():
            _write_table_to_csv(f"{self.file_name}_{name}", table, Path(file_directory))

    def to_json(self, *tables: str) -> str:
        """Generate a json compliant string representation of tables in the XER file

        Returns:
            str: json compliant string representation of XER tables
        """
        out_data = {}
        if not tables:
            out_data = self.tables
        else:
            out_data = {
                name: table for name, table in self.tables.items() if name in tables
            }
        json_data = {self.file_name: {**out_data}}
        return json.dumps(json_data, indent=4)


def _write_table_to_csv(name: str, table: dict, file_directory: Path) -> None:
    labels = list(list(table.values())[0].keys())
    with file_directory.joinpath(f"{name}.csv").open("w") as f:
        writer = csv.DictWriter(f, fieldnames=labels, delimiter="\t")
        writer.writeheader()
        for row in table.values():
            writer.writerow(row)
    f.close()


def _clean_id_label(label: str) -> str | None:
    prefixes = ("base_", "last_", "new_", "parent_", "pred_")
    for prefix in prefixes:
        if label.startswith(prefix):
            return label.replace(prefix, "")
    return


def _parse_file_info(data: str) -> list[str]:
    ermhdr = re.search(r"(?<=ERMHDR\t).+", data)
    if not ermhdr:
        raise ValueError("Invalid XER File")
    return ermhdr.group().split("\t")


def _parse_table(table: str) -> dict[str, dict[int, dict[str, str]]]:
    """Parse table name, columns, and rows"""

    lines: list[str] = table.split("\n")
    name = lines.pop(0).strip()  # First line is the table name
    cols = lines.pop(0).strip().split("\t")[1:]  # Second line is the column labels
    data = [dict(zip(cols, _split_row(row))) for row in lines if row.startswith("%R")]

    unique_id = TableInfo[name].value["key"]
    return {
        name: {
            int(entry[unique_id]) if unique_id else i: entry
            for i, entry in enumerate(data, 1)
        }
    }


def _read_file(file: str | Path | BinaryIO) -> tuple[str, str]:
    file_contents = ""
    file_name = ""
    if isinstance(file, (str, Path)):
        # Path directory to file
        file_name = Path(file).stem
        with open(file, encoding=XerReader.CODEC, errors="ignore") as f:
            file_contents = f.read()
    else:
        # Binary file from requests, Flask, FastAPI, etc...
        file_contents = file.read().decode(XerReader.CODEC, errors="ignore")
        file_name = file.name

    if not file_contents.startswith("ERMHDR"):
        raise ValueError("ValueError: invalid XER file")

    return file_name, file_contents


def _split_row(row: str) -> list[str]:
    """Splits row into values."""
    row_values = row.split("\t")[1:]
    if row_values:
        row_values[-1] = _strip_value(row_values[-1])
    return row_values


def _strip_value(val: str) -> str:
    """Strips white space from a value"""
    if val == "":
        return ""
    return val.strip()
