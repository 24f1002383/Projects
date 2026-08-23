import csv
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../src")
    )
)

import database
import main

from database import (
    create_table,
    get_expenses,
)


class TestMain(unittest.TestCase):

    def setUp(self):
        self.test_db = tempfile.NamedTemporaryFile(
            suffix=".db",
            delete=False
        )

        self.test_db.close()

        database.DATABASE = self.test_db.name

        create_table()

    def tearDown(self):
        if os.path.exists(self.test_db.name):
            os.remove(self.test_db.name)

    def test_import_expenses_from_csv(self):
        csv_file = tempfile.NamedTemporaryFile(
            suffix=".csv",
            delete=False,
            mode="w",
            newline="",
            encoding="utf-8"
        )

        writer = csv.writer(csv_file)

        writer.writerow(
            [
                "ID",
                "Amount",
                "Category",
                "Description",
                "Date",
            ]
        )

        writer.writerow(
            [
                "1",
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        )

        writer.writerow(
            [
                "2",
                "750",
                "Travel",
                "Bus",
                "2026-08-22",
            ]
        )

        csv_file.close()

        with patch(
            "builtins.input",
            return_value=csv_file.name
        ):
            main.import_expenses_from_csv()

        expenses = get_expenses()

        self.assertEqual(len(expenses), 2)
        self.assertEqual(expenses[0][1], 500)
        self.assertEqual(expenses[0][2], "Food")
        self.assertEqual(expenses[0][3], "Lunch")
        self.assertEqual(expenses[0][4], "2026-08-21")

        self.assertEqual(expenses[1][1], 750)
        self.assertEqual(expenses[1][2], "Travel")
        self.assertEqual(expenses[1][3], "Bus")
        self.assertEqual(expenses[1][4], "2026-08-22")

        os.remove(csv_file.name)

    def test_import_invalid_csv(self):
        csv_file = tempfile.NamedTemporaryFile(
            suffix=".csv",
            delete=False,
            mode="w",
            newline="",
            encoding="utf-8"
        )

        writer = csv.writer(csv_file)

        writer.writerow(
            [
                "Wrong",
                "Columns",
            ]
        )

        writer.writerow(
            [
                "test",
                "data",
            ]
        )

        csv_file.close()

        with patch(
            "builtins.input",
            return_value=csv_file.name
        ):
            main.import_expenses_from_csv()

        expenses = get_expenses()

        self.assertEqual(len(expenses), 0)

        os.remove(csv_file.name)

    def test_import_skips_invalid_rows(self):
        csv_file = tempfile.NamedTemporaryFile(
            suffix=".csv",
            delete=False,
            mode="w",
            newline="",
            encoding="utf-8"
        )

        writer = csv.writer(csv_file)

        writer.writerow(
            [
                "ID",
                "Amount",
                "Category",
                "Description",
                "Date",
            ]
        )

        writer.writerow(
            [
                "1",
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        )

        writer.writerow(
            [
                "2",
                "-100",
                "Food",
                "Invalid",
                "2026-08-21",
            ]
        )

        writer.writerow(
            [
                "3",
                "abc",
                "Food",
                "Invalid",
                "2026-08-21",
            ]
        )

        writer.writerow(
            [
                "4",
                "300",
                "",
                "Invalid",
                "2026-08-21",
            ]
        )

        writer.writerow(
            [
                "5",
                "200",
                "Travel",
                "Bus",
                "invalid-date",
            ]
        )

        csv_file.close()

        with patch(
            "builtins.input",
            return_value=csv_file.name
        ):
            main.import_expenses_from_csv()

        expenses = get_expenses()

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0][1], 500)
        self.assertEqual(expenses[0][2], "Food")

        os.remove(csv_file.name)

    def test_import_empty_filename(self):
        with patch(
            "builtins.input",
            return_value=""
        ):
            main.import_expenses_from_csv()

        expenses = get_expenses()

        self.assertEqual(len(expenses), 0)

    def test_import_file_not_found(self):
        with patch(
            "builtins.input",
            return_value="does_not_exist.csv"
        ):
            main.import_expenses_from_csv()

        expenses = get_expenses()

        self.assertEqual(len(expenses), 0)


if __name__ == "__main__":
    unittest.main()