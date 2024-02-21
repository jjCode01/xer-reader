"""
Unittests for xer-reader.

Setup the config.py file - follow instructions in config_template.py

Each unittest will run through all .xer file in the specified directory, 
create an instance of XerReader, and run the assertion tests. 
"""

import re
import unittest
from datetime import datetime
from pathlib import Path

from tqdm import tqdm

import tests.config as config
from xer_reader.src.reader import XerReader

date_format = "%Y-%m-%d"


def get_xer_files() -> list:
    # Pull location of xer files from config file
    xer_file_path = Path(config.directory)

    # Verify location of xer files is valid
    if not xer_file_path.exists():
        raise FileNotFoundError(f"Could not find the directory {config.directory}")

    # Get list of xer files
    xer_files = [file for file in Path(config.directory).glob("**/*.xer")]
    if not xer_files:
        raise FileNotFoundError(f"No .xer files found in {xer_file_path.absolute()}")

    return xer_files


class TestReader(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_folder = Path.cwd().joinpath("temp")
        self.files = get_xer_files()

    def tearDown(self) -> None:
        """Remove temporary files created during the test."""
        if self.temp_folder.is_dir():
            for file in self.temp_folder.glob("*.*"):
                Path.unlink(file)
            # self.temp_folder.rmdir()

    def test_reader(self):
        print(f"Running XER Reader tests on {len(self.files)} .xer files.")
        for file in tqdm(self.files):
            reader = XerReader(file)
            tables = reader.to_dict()
            self.assertIsInstance(reader.export_date, datetime)
            self.assertRegex(reader.export_version, re.compile(r"\d+\.\d+"))
            for table in tables:
                self.assertGreaterEqual(len(table), 1)

    def test_delete_table(self):
        print(f"Running delete_table tests on {len(self.files)} .xer files.")
        for file in tqdm(self.files):
            reader = XerReader(file)
            tables = reader.to_dict()
            for table in tables.keys():
                self.assertNotIn("%T\t{table}\n", reader.delete_tables(table))

    def test_get_table_str(self):
        print(f"Running get_table_str tests on {len(self.files)} .xer files.")
        for file in tqdm(self.files):
            reader = XerReader(file)
            self.assertEqual(reader.get_table_str("TEST_TABLE"), "")
            self.assertEqual(reader.get_table_str("CALENDAR")[:8], "clndr_id")
            self.assertEqual(reader.get_table_str("PROJECT")[:7], "proj_id")
            self.assertEqual(reader.get_table_str("PROJWBS")[:6], "wbs_id")

    def test_to_csv(self):
        print(f"Running to_csv tests on {len(self.files)} .xer files.")
        for file in tqdm(self.files):
            reader = XerReader(file)
            tables = reader.to_dict()
            temp_folder = Path.cwd().joinpath("temp")
            if not temp_folder.is_dir():
                Path.mkdir(temp_folder)

            reader.to_csv(temp_folder)

            for table_name in tables.keys():
                csv_file = temp_folder.joinpath(f"{reader.file_name}_{table_name}.csv")
                self.assertTrue(
                    csv_file.is_file(),
                    f"{table_name}.csv",
                )
                if csv_file.is_file():
                    Path.unlink(csv_file)

    def test_to_excel(self):
        print(f"Running to_excel tests on {len(self.files)} .xer files.")
        for file in tqdm(self.files):
            reader = XerReader(file)
            temp_folder = Path.cwd().joinpath("temp")
            if not temp_folder.is_dir():
                Path.mkdir(temp_folder)

            reader.to_excel(temp_folder)

            excel_file = temp_folder.joinpath(f"{reader.file_name}.xlsx")
            self.assertTrue(
                excel_file.is_file(),
                f"{reader.file_name}.xlsx",
            )
            if excel_file.is_file():
                Path.unlink(excel_file)
