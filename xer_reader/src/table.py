from datetime import datetime
from typing import Any

from xer_reader.src.table_data import table_data

DATE_HR_FORMAT = "%Y-%m-%d %H:%M"


class UnrecognizedTable(Exception):
    def __init__(self, table: str) -> None:
        self.table = table
        self.message = f"Unregognized Table: {self.table}"

    def __str__(self) -> str:
        return self.message


class XerTable:
    """A class representing a P6 table"""

    def __init__(self, data: str) -> None:
        _lines: list[str] = data.split("\n")

        # First line is the table name
        self.name: str = _lines.pop(0).strip()
        """Table Name"""

        if self.name not in table_data:
            raise UnrecognizedTable(self.name)

        self.depends: list[str] = table_data[self.name]["depends"]
        """List of Required Foreign Tables"""
        self.description: str = table_data[self.name]["description"]
        """Discription of Data Contained in Table"""
        self.key: str | None = table_data[self.name]["key"]
        """Label Name for Unique ID of Table Entries"""

        # Second line is the column labels
        self.labels: list[str] = _lines.pop(0).strip().split("\t")[1:]
        """List Entry Labels or Column Headers"""

        # Remaining lines are the data rows
        self.rows: list[list[str]] = [
            _split_row(row) for row in _lines if row.startswith("%R")
        ]
        """Nested Array containing Rows of Data"""

        self._entries: list[dict[str, Any]] = []
        self._serialized: bool = False

    def __bool___(self) -> bool:
        return len(self.rows) > 0

    def __getitem__(self, _key):
        if isinstance(_key, (int, slice)):
            return self.rows[_key]

        if isinstance(_key, str):
            if _key not in self.labels:
                raise KeyError(f"{_key} not found")

            return [row[_key] for row in self.entries()]

        if isinstance(_key, (list, tuple, set)):
            for k in _key:
                if k not in self.labels:
                    raise KeyError("{k} not found")

            return [{k: row[k] for k in _key} for row in self.entries()]

    def __len__(self) -> int:
        return len(self.rows)

    def __str__(self) -> str:
        return self.name

    def entries(self, serialize: bool = False) -> list[dict[str, str]]:
        if not self._entries or serialize != self._serialized:
            self._entries = [
                _converter(serialize, **dict(zip(self.labels, row)))
                for row in self.rows
            ]
        self._serialized = serialize
        return self._entries


def _converter(
    serialize: bool, **kwargs: str
) -> dict[str, None | int | float | datetime | bool]:
    return {
        label: _convert_entry_data_type(label, value, serialize)
        for label, value in kwargs.items()
    }


def _is_date_label(label: str) -> bool:
    return label.endswith(("_date", "_date2"))


def _is_float_label(label: str) -> bool:
    return label.endswith(
        ("_cost", "_hr", "_pct", "_qty", "_qty2", "_qty3", "_qty4", "_qty5", "_rate")
    )


def _is_int_label(label: str) -> bool:
    return label.endswith(
        ("_id", "_base", "_cnt", "_len", "_num", "_order", "_path", "_step")
    )


def _convert_entry_data_type(
    label: str, value: str, serialize: bool
) -> None | int | float | datetime | bool:
    if value == "":
        return None

    if _is_int_label(label):
        return int(value)
    if _is_float_label(label):
        return float(value)
    if not serialize and _is_date_label(label):
        return datetime.strptime(value, DATE_HR_FORMAT)
    if label.endswith("_flag"):
        return value == "Y"

    return value


def _split_row(row: str) -> list[str]:
    """Splits row into values."""
    if not row.startswith("%R"):
        raise ValueError("Invalid Row Data")

    row_values = row.split("\t")[1:]
    if row_values:
        row_values[-1] = _strip_value(row_values[-1])

    return row_values


def _strip_value(val: str) -> str:
    """Strips white space from a value"""
    if val == "":
        return ""
    return val.strip()
