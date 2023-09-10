import json
import unittest

from multiprocessing import Pool
from pathlib import Path
from tqdm import tqdm

import tests.config as config

from xer_reader.src.reader import Reader

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
    reader = Reader(file)

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


def process_xer_file(xer: Reader) -> dict:
    return {
        "export_date": xer.export_date.strftime(date_format),
        "export_version": xer.export_version,
        "table_names": xer.table_names(),
    }


class TestReader(unittest.TestCase):
    def setUp(self) -> None:
        self.xer_files: Path = Path(r"./tests/fixtures/xer_files.json")

        if not self.xer_files.is_file():
            print("Creating xer data json file...")
            create_test_file(self.xer_files, generate_test_xer_file_data)

    def test_reader(self):
        with self.xer_files.open() as f:
            xer_data: dict = json.load(f)

        print(f"Running tests on {len(xer_data)} .xer files.")
        for file, data in tqdm(xer_data.items()):
            reader = Reader(file)
            self.assertEqual(
                reader.export_date.strftime(date_format), data["export_date"]
            )
            self.assertEqual(
                reader.export_version, data["export_version"]
            )
