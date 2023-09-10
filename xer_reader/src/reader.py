# xer-reader
# reader.py

from datetime import datetime
from enum import Enum
from pathlib import Path
import re
from typing import BinaryIO


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
        self.data: str = _read(file)

        _file_info = _parse_file_info(self.data)
        self.export_version: str = _file_info[0]
        self.export_date: datetime = datetime.strptime(_file_info[1], "%Y-%m-%d")

    def all_tables(self) -> dict[str, list[dict[str, str]]]:
        """Returns a dictionary of all tables with a list of their entries"""
        return {name: self.get_table(name) for name in self.table_names()}

    def has_table(self, table_name: str) -> bool:
        """Check if table is included in xer file"""
        return f"%T\t{table_name.upper()}" in self.data

    def get_table(self, table_name: str) -> list[dict[str, str]]:
        """Returns a list of entries from a table"""
        search = re.compile(rf"(?<=%T\t{table_name.upper()}\n)(.|\s)*?(?=%T|%E)")
        table = search.search(self.data)
        if not table:
            return []
        return _parse_table_data(table.group())

    def table_names(self) -> list[str]:
        """Returns a list of table names included in the xer file"""
        return RegEx.table_names.value.findall(self.data)


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


def _parse_table_data(data: str) -> list[dict[str, str]]:
    lines = data.split("\n")
    cols = lines.pop(0).strip().split("\t")[1:]  # Second line is the column labels
    rows = [dict(zip(cols, _clean_row(row))) for row in lines if row.startswith("%R")]
    return rows


def _read(file: str | Path | BinaryIO) -> str:
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
