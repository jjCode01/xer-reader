import json
import re
import unittest

from datetime import datetime
from multiprocessing import Pool
from pathlib import Path
from tqdm import tqdm

import tests.config as config

from xer_reader.src.reader import XerReader

date_format = "%Y-%m-%d"


def create_test_file(test_file: Path, func) -> None:
    xer_files = get_xer_files()

    with Pool() as p:
        data_list = list(
            tqdm(
                p.imap(func, xer_files),
                total=len(xer_files),
            )
        )

    data_dict = {key: data for item in data_list for key, data in item.items()}

    json_data = json.dumps(data_dict, indent=4)

    with test_file.open("w") as outfile:
        outfile.write(json_data)


def generate_test_xer_file_data(file: Path) -> dict:
    reader = XerReader(file)

    return {
        str(file.absolute()): {
            **process_xer_file(reader),
        }
    }


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


def process_xer_file(xer: XerReader) -> dict:
    return {
        "export_date": xer.export_date.strftime(date_format),
        "export_user": xer.export_user,
        "export_version": xer.export_version,
        "errors": xer.check_errors(),
        **{name: len(entries) for name, entries in xer.tables.items()},
    }


class TestReader(unittest.TestCase):
    def setUp(self) -> None:
        self.xer_files: Path = Path(r"./tests/fixtures/xer_files.json")
        self.temp_folder = Path.cwd().joinpath("temp")
        self.files = get_xer_files()

        if not self.xer_files.is_file():
            print("Creating xer data json file...")
            create_test_file(self.xer_files, generate_test_xer_file_data)

    def tearDown(self) -> None:
        if self.temp_folder.is_dir():
            for file in self.temp_folder.glob("*.*"):
                Path.unlink(file)
            self.temp_folder.rmdir()

    def test_reader(self):
        print(f"Running XER Reader tests on {len(self.files)} .xer files.")
        for file in tqdm(self.files):
            reader = XerReader(file)
            self.assertIsInstance(reader.export_date, datetime)
            self.assertRegex(reader.export_version, re.compile(r"\d+\.\d+"))
            for table in reader.tables.values():
                self.assertGreaterEqual(len(table), 1)
            

    def test_delete_table(self):
        print(f"Running delete_table tests on {len(self.files)} .xer files.")
        for file in tqdm(self.files):
            reader = XerReader(file)
            for table in reader.tables.keys():
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
            temp_folder = Path.cwd().joinpath("temp")
            if not temp_folder.is_dir():
                Path.mkdir(temp_folder)

            reader.to_csv(temp_folder)

            for table_name in reader.tables.keys():
                csv_file = temp_folder.joinpath(f"{reader.file_name}_{table_name}.csv")
                self.assertTrue(
                    csv_file.is_file(),
                    f"{table_name}.csv",
                )
                if csv_file.is_file():
                    Path.unlink(csv_file)
