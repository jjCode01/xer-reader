# xer-reader
# reader.py

from datetime import datetime
from enum import Enum
from pathlib import Path
import re
from typing import BinaryIO

from xer_reader.src.table_info import TableInfo


REQUIRED_TABLES = {"CALENDAR", "PROJECT", "PROJWBS", "TASK", "TASKPRED"}


class RegEx(Enum):
    file_version = re.compile(r"(?<=ERMHDR\t)\d+\.\d+")
    table_names = re.compile(r"(?<=%T\t)[A-Z]+")
    ermhdr = re.compile(r"(?<=ERMHDR\t).+")


def _parse_file_info(data: str) -> list:
    ermhdr = RegEx.ermhdr.value.search(data)
    if not ermhdr:
        raise ValueError("Invalid XER File")
    return ermhdr.group().split("\t")


class Reader:
    CODEC = "cp1252"

    def __init__(self, file: str | Path | BinaryIO) -> None:
        self.data: str = _read_file(file)

        _file_info = _parse_file_info(self.data)
        self.export_version: str = _file_info[0]
        self.export_date: datetime = datetime.strptime(_file_info[1], "%Y-%m-%d")
        self.export_user: str = _file_info[4]
        self.tables: dict[str, dict[str, dict[str, str]]] = {
            name: rows
            for table in self.data.split("%T\t")[1:]
            for name, rows in _parse_table(table).items()
        }

    def errors(self) -> list[str]:
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
                    if val != "" and key.endswith("_id"):
                        clean_key = _clean_id_label(key)
                        if clean_key != "pobs_parent_id" and val not in self.tables.get(id_map[clean_key], {}):
                            if key == "parent_wbs_id" and row["proj_node_flag"] == "Y":
                                continue
                            errors.add(f"Orphan data {key} [{val}] in table {table}")

        return list(errors)

    def to_csv(self):
        # TODO
        pass

def _clean_id_label(val: str) -> str:
    prefixes = ("base_", "last_", "new_", "parent_", "pred_", "sum_base_")
    for prefix in prefixes:
        if val.startswith(prefix):
            return val.replace(prefix, "")
        
    if val == "fk_id":
        return "task_id"
    # if val.startswith("parent_"):
    #     return val.replace("parent_", "")
    # if val.startswith("pred_"):
    #     return val.replace("pred_", "")
    # if val.startswith("base_"):
    #     return val.replace("base_", "")
    
    return val


def _clean_row(row: str) -> list[str]:
    """Strips white space from last value in row"""
    row_values = row.split("\t")[1:]
    if row_values:
        row_values[-1] = _clean_value(row_values[-1])
    return row_values


def _clean_value(val: str) -> str:
    """Strips white space from a value"""
    if val == "":
        return ""
    return val.strip()


def _parse_table(table: str) -> dict[str, dict[str, dict[str, str]]]:
    """Parse table name, columns, and rows"""

    lines: list[str] = table.split("\n")
    name = lines.pop(0).strip()  # First line is the table name
    cols = lines.pop(0).strip().split("\t")[1:]  # Second line is the column labels
    data = [dict(zip(cols, _clean_row(row))) for row in lines if row.startswith("%R")]

    unique_id = TableInfo[name].value["key"]
    return {
        name: {
            entry[unique_id] if unique_id else str(i): entry
            for i, entry in enumerate(data, 1)
        }
    }


def _read_file(file: str | Path | BinaryIO) -> str:
    file_contents = ""
    if isinstance(file, (str, Path)):
        # Path directory to file
        with open(file, encoding=Reader.CODEC, errors="ignore") as f:
            file_contents = f.read()
    else:
        # Binary file from requests, Flask, FastAPI, etc...
        file_contents = file.read().decode(Reader.CODEC, errors="ignore")

    if not file_contents.startswith("ERMHDR"):
        raise ValueError("ValueError: invalid XER file")

    return file_contents
