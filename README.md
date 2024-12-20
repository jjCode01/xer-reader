# Xer-Reader

Read the contents of a Primavera P6 XER file using Python.

Xer-Reader makes it easy to read, parse, and convert the data in a XER file to other formats.

_Refer to the [Oracle Documentation](https://docs.oracle.com/cd/F25600_01/English/Mapping_and_Schema/xer_import_export_data_map_project/index.htm) for more information regarding how data is mapped to the XER format.  
Tested on XER files exported as versions 15.2 through 19.12._

## Install

**Windows**:

```bash
pip install xer-reader
```

**Linux/Mac**:

```bash
pip3 install xer-reader
```

## Usage

Import the `XerReader` class from `xer_reader`.

```python
from xer_reader import XerReader
```

Create a new instance of an `XerReader` object by passing in the XER file as an argument. `XerReader` can accept the file path represented as a `str` or pathlib `Path` object, or a Binary file received as a response from requests, Flask, FastAPI, etc...

```python
file = r"/path/to/file.xer"
reader = XerReader(file)
```

### Attributes

- `data` [str] - _The contents of the XER file as a string._
- `export_date` [datetime] - _The date the XER file was exported._
- `export_user` [str] - _The P6 user who export the XER file._
- `export_version` [str] - _The P6 verison used to export the XER file._
- `file_name` [str] - _The name of the file without the '.xer' extension._

### Methods

**`check_errors()`** -> _list[str]_  
Checks the XER file for missing tables and orphan data, and returns the results as a list of errors.

- Missing tables can occur when an entry in _Table 1_ points to an entry in _Table 2_ but _Table 2_ does not exist at all.
- Orphan data occurs when an entry in _Table 1_ points to an entry _Table 2_ but the entry in _Table 2_ does not exist.

**`delete_tables(*table_names: str)`** -> _str_  
Delete a variable number of tables (_table_names_) from the XER file data and returns a new string (_Does not modify `XerReader.data` attribute_).

In the following example the tables associated with User Defined Fields are removed from the XER file contents and stored in a new variable `new_xer_data`, which can then be written to a new XER file:

```python
new_xer_data = reader.delete_tables("UDFTYPE", "UDFVALUE")

with open("New_XER.xer", "w", encoding=XerReader.CODEC) as new_xer_file:
    new_xer_file.write(new_xer_data)
```

**`get_table_names()`** -> _list[str]_  
Returns a list of table names included in the XER file.

**`get_table_str(table_name: str)`** -> _str_  
Returns the tab seperated text for a specific table in the XER file.

**`has_table(table_name: str)`** -> _bool_  
Return True if table (`table_name`) if found in the XER file.

**`to_dict()`** -> _dict[str, Table]_  
Returns a dictionary with the table name as the key and a `Table` object as the value.

**`to_csv(file_directory: str | Path, table_names: list[str], delimeter: str)`** -> _None_  
Generate a CSV file for each table in the XER file. CSV files will be created in the current working directory.  
Optional `file_directory`: Pass a string or Path object to specify a folder to store the CSV files in.  
Optional `table_names`: List of tables names to save to CSV files.  
Optional `delimeter`: Change the default delimeter from a `tab` to another string (e.g. a coma ",").

```python
reader.to_csv(table_names=["TASK", "PROJWBS"], delimeter=",")
```

**`to_excel()`** -> _None_  
Generate an Excel (.xlsx) file with each table in the XER file on its own spreadsheet. The Excel file will be create in the
current working directory.

**`to_json(*tables: str)`** -> _str_  
Generate a json compliant string representation of the tables in the XER file.  
Optional: Pass in specific table names to include in the json string.
