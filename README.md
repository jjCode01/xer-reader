# Xer-Reader

Read the contents of a Primavera P6 XER file using Python.  

Xer-Reader makes it easy to read, parse, and convert the data in a XER file to other formats.

*Refer to the [Oracle Documentation]( https://docs.oracle.com/cd/F25600_01/English/Mapping_and_Schema/xer_import_export_data_map_project/index.htm) for more information regarding how data is mapped to the XER format.  
Tested on XER files exported as versions 15.2 through 19.12.*  

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

* `data` [str] - *The contents of the XER file as a string.*
* `export_date` [datetime] - *The date the XER file was exported.*
* `export_user` [str] - *The P6 user who export the XER file.*
* `export_version` [str] - *The P6 verison used to export the XER file.*
* `file_name` [str] - *The name of the file without the '.xer' extension.*

### Methods

**`check_errors()`** -> *list[str]*  
Checks the XER file for missing tables and orphan data, and returns the results as a list of errors.  

* Missing tables can occur when an entry in *Table 1* points to an entry in *Table 2* but *Table 2* does not exist at all.
* Orphan data occurs when an entry in *Table 1* points to an entry *Table 2* but the entry in *Table 2* does not exist.

**`delete_tables(*table_names: str)`** -> *str*  
Delete a variable number of tables (*table_names*) from the XER file data and returns a new string (*Does not modify `XerReader.data` attribute*).  

In the following example the tables associated with User Defined Fields are removed from the XER file contents and stored in a new variable `new_xer_data`, which can then be written to a new XER file:
```python
new_xer_data = reader.delete_tables("UDFTYPE", "UDFVALUE")

with open("New_XER.xer", "w", encoding=XerReader.CODEC) as new_xer_file:
    new_xer_file.write(new_xer_data)
```

**`get_table_names()`** -> *list[str]*  
Returns a list of table names included in the XER file.  

**`get_table_str(table_name: str)`** -> *str*  
Returns the tab seperated text for a specific table in the XER file.

**`has_table(table_name: str)`** -> *bool*  
Return True if table (`table_name`) if found in the XER file.

**`parse_tables()`** -> *dict[str, Table]*  
Returns a dictionary with the table name as the key and a `Table` object as the value.  

**`to_csv(file_directory: str | Path)`** -> *None*  
Generate a CSV file for each table in the XER file using 'tab' as the delimiter. CSV files will be created in the current working directory.   
Optional: Pass a string or Path object (`file_directory`) to speficy a folder to store the CSV files in.  

**`to_json(*tables: str)`** -> *str*  
Generate a json compliant string representation of the tables in the XER file.  
Optional: Pass in specific table names to include in the json string.
