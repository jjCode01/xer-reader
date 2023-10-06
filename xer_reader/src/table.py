from xer_reader.src.table_info import TableInfo


class Table:
    """A class representing a P6 table"""

    description: str
    entries: list[dict[str, str]]
    labels: list[str]
    key: str | None
    name: str

    def __init__(
        self, name: str, labels: list[str], entries: list[dict[str, str]]
    ) -> None:
        self.name = name
        self.entries = entries
        self.labels = labels
        try:
            self.description = TableInfo[name].value["description"]
            self.key = TableInfo[name].value["key"]
        except KeyError:
            self.description = ""
            self.key = None

    def __bool___(self) -> bool:
        return len(self.entries) > 0

    def __len__(self) -> int:
        return len(self.entries)

    def __str__(self) -> str:
        return self.name
