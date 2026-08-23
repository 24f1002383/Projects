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

    def create_csv_file(self, rows):
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

        writer.writerows(rows)
        csv_file.close()

        return csv_file.name

    def test_validate_date_valid(self):
        self.assertTrue(
            main.validate_date("2026-08-21")
        )

    def test_validate_date_invalid(self):
        self.assertFalse(
            main.validate_date("21-08-2026")
        )

    def test_validate_month_valid(self):
        self.assertTrue(
            main.validate_month("2026-08")
        )

    def test_validate_month_invalid(self):
        self.assertFalse(
            main.validate_month("2026-8")
        )

    def test_validate_month_invalid_month(self):
        self.assertFalse(
            main.validate_month("2026-13")
        )

    def test_add_new_expense(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.add_new_expense()

        expenses = get_expenses()

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0][1], 500)
        self.assertEqual(expenses[0][2], "Food")
        self.assertEqual(expenses[0][3], "Lunch")
        self.assertEqual(
            expenses[0][4],
            "2026-08-21"
        )

    def test_add_expense_invalid_amount(self):
        with patch(
            "builtins.input",
            return_value="abc"
        ):
            main.add_new_expense()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_add_expense_negative_amount(self):
        with patch(
            "builtins.input",
            return_value="-100"
        ):
            main.add_new_expense()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_add_expense_zero_amount(self):
        with patch(
            "builtins.input",
            return_value="0"
        ):
            main.add_new_expense()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_add_expense_empty_category(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.add_new_expense()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_add_expense_invalid_date(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "Food",
                "Lunch",
                "invalid-date",
            ]
        ):
            main.add_new_expense()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_add_expense_invalid_date_format(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "Food",
                "Lunch",
                "21-08-2026",
            ]
        ):
            main.add_new_expense()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_update_existing_expense(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.add_new_expense()

        with patch(
            "builtins.input",
            side_effect=[
                "1",
                "750",
                "Travel",
                "Bus",
                "2026-08-22",
            ]
        ):
            main.update_existing_expense()

        expenses = get_expenses()

        self.assertEqual(
            expenses[0][1],
            750
        )

        self.assertEqual(
            expenses[0][2],
            "Travel"
        )

        self.assertEqual(
            expenses[0][3],
            "Bus"
        )

        self.assertEqual(
            expenses[0][4],
            "2026-08-22"
        )

    def test_update_non_existing_expense(self):
        with patch(
            "builtins.input",
            side_effect=[
                "999",
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.update_existing_expense()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_update_invalid_expense_id(self):
        with patch(
            "builtins.input",
            return_value="abc"
        ):
            main.update_existing_expense()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_update_negative_amount(self):
        with patch(
            "builtins.input",
            side_effect=[
                "1",
                "-500",
            ]
        ):
            main.update_existing_expense()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_update_empty_category(self):
        with patch(
            "builtins.input",
            side_effect=[
                "1",
                "500",
                "",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.update_existing_expense()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_update_invalid_date(self):
        with patch(
            "builtins.input",
            side_effect=[
                "1",
                "500",
                "Food",
                "Lunch",
                "invalid-date",
            ]
        ):
            main.update_existing_expense()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_delete_existing_expense(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.add_new_expense()

        with patch(
            "builtins.input",
            return_value="1"
        ):
            main.delete_existing_expense()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_delete_non_existing_expense(self):
        with patch(
            "builtins.input",
            return_value="999"
        ):
            main.delete_existing_expense()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_delete_invalid_expense_id(self):
        with patch(
            "builtins.input",
            return_value="abc"
        ):
            main.delete_existing_expense()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_search_existing_expenses(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.add_new_expense()

        with patch(
            "builtins.input",
            return_value="Food"
        ):
            main.search_existing_expenses()

        expenses = database.search_expenses(
            "Food"
        )

        self.assertEqual(
            len(expenses),
            1
        )

    def test_search_empty_category(self):
        with patch(
            "builtins.input",
            return_value=""
        ):
            main.search_existing_expenses()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_search_no_results(self):
        with patch(
            "builtins.input",
            return_value="Travel"
        ):
            main.search_existing_expenses()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_search_by_date(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.add_new_expense()

        with patch(
            "builtins.input",
            return_value="2026-08-21"
        ):
            main.search_expenses_by_date_menu()

        expenses = database.search_expenses_by_date(
            "2026-08-21"
        )

        self.assertEqual(
            len(expenses),
            1
        )

    def test_search_by_invalid_date(self):
        with patch(
            "builtins.input",
            return_value="invalid-date"
        ):
            main.search_expenses_by_date_menu()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_search_by_date_no_results(self):
        with patch(
            "builtins.input",
            return_value="2026-08-30"
        ):
            main.search_expenses_by_date_menu()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_set_budget(self):
        with patch(
            "builtins.input",
            side_effect=[
                "2026-08",
                "5000",
            ]
        ):
            main.set_budget()

        status = database.get_budget_status(
            "2026-08"
        )

        self.assertEqual(
            status["budget"],
            5000
        )

    def test_set_invalid_budget(self):
        with patch(
            "builtins.input",
            side_effect=[
                "2026-08",
                "-100",
            ]
        ):
            main.set_budget()

        self.assertIsNone(
            database.get_monthly_budget(
                "2026-08"
            )
        )

    def test_set_zero_budget(self):
        with patch(
            "builtins.input",
            side_effect=[
                "2026-08",
                "0",
            ]
        ):
            main.set_budget()

        self.assertIsNone(
            database.get_monthly_budget(
                "2026-08"
            )
        )

    def test_set_budget_invalid_amount(self):
        with patch(
            "builtins.input",
            side_effect=[
                "2026-08",
                "abc",
            ]
        ):
            main.set_budget()

        self.assertIsNone(
            database.get_monthly_budget(
                "2026-08"
            )
        )

    def test_set_budget_invalid_month(self):
        with patch(
            "builtins.input",
            side_effect=[
                "invalid-month",
            ]
        ):
            main.set_budget()

        self.assertIsNone(
            database.get_monthly_budget(
                "invalid-month"
            )
        )

    def test_set_budget_short_month(self):
        with patch(
            "builtins.input",
            side_effect=[
                "2026-8",
            ]
        ):
            main.set_budget()

        self.assertIsNone(
            database.get_monthly_budget(
                "2026-8"
            )
        )

    def test_show_budget_status_without_budget(self):
        with patch(
            "builtins.input",
            return_value="2026-08"
        ):
            main.show_budget_status()

    def test_show_budget_status_invalid_month(self):
        with patch(
            "builtins.input",
            return_value="invalid-month"
        ):
            main.show_budget_status()

    def test_show_budget_status_exceeded(self):
        with patch(
            "builtins.input",
            side_effect=[
                "2026-08",
                "500",
            ]
        ):
            main.set_budget()

        with patch(
            "builtins.input",
            side_effect=[
                "5000",
                "Food",
                "Shopping",
                "2026-08-21",
            ]
        ):
            main.add_new_expense()

        with patch(
            "builtins.input",
            return_value="2026-08"
        ):
            main.show_budget_status()

    def test_monthly_summary_invalid_month(self):
        with patch(
            "builtins.input",
            return_value="invalid-month"
        ):
            main.show_monthly_summary()

    def test_monthly_summary_short_month(self):
        with patch(
            "builtins.input",
            return_value="2026-8"
        ):
            main.show_monthly_summary()

    def test_monthly_summary_no_expenses(self):
        with patch(
            "builtins.input",
            return_value="2026-08"
        ):
            main.show_monthly_summary()

    def test_monthly_summary(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.add_new_expense()

        with patch(
            "builtins.input",
            return_value="2026-08"
        ):
            main.show_monthly_summary()

    def test_export_expenses_to_csv(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.add_new_expense()

        csv_path = os.path.join(
            tempfile.gettempdir(),
            "expense_test_export.csv"
        )

        try:
            with patch(
                "builtins.input",
                return_value=csv_path
            ):
                main.export_expenses_to_csv()

            self.assertTrue(
                os.path.exists(csv_path)
            )

            with open(
                csv_path,
                "r",
                encoding="utf-8"
            ) as file:
                rows = list(
                    csv.reader(file)
                )

            self.assertEqual(
                rows[0],
                [
                    "ID",
                    "Amount",
                    "Category",
                    "Description",
                    "Date",
                ]
            )

            self.assertEqual(
                rows[1][1],
                "500.0"
            )

        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)

    def test_export_without_csv_extension(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.add_new_expense()

        base_path = os.path.join(
            tempfile.gettempdir(),
            "expense_extension_test"
        )

        csv_path = base_path + ".csv"

        try:
            with patch(
                "builtins.input",
                return_value=base_path
            ):
                main.export_expenses_to_csv()

            self.assertTrue(
                os.path.exists(csv_path)
            )

        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)

    def test_export_empty_database(self):
        with patch(
            "builtins.input",
            return_value="expenses.csv"
        ):
            main.export_expenses_to_csv()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_import_empty_filename(self):
        with patch(
            "builtins.input",
            return_value=""
        ):
            main.import_expenses_from_csv()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_import_file_not_found(self):
        with patch(
            "builtins.input",
            return_value="does_not_exist.csv"
        ):
            main.import_expenses_from_csv()

        self.assertEqual(
            len(get_expenses()),
            0
        )

    def test_import_invalid_csv(self):
        csv_path = tempfile.NamedTemporaryFile(
            suffix=".csv",
            delete=False,
            mode="w",
            newline="",
            encoding="utf-8"
        )

        writer = csv.writer(csv_path)

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

        csv_path.close()

        try:
            with patch(
                "builtins.input",
                return_value=csv_path.name
            ):
                main.import_expenses_from_csv()

            self.assertEqual(
                len(get_expenses()),
                0
            )

        finally:
            os.remove(csv_path.name)

    def test_import_skips_invalid_rows(self):
        csv_path = self.create_csv_file(
            [
                [
                    "1",
                    "500",
                    "Food",
                    "Lunch",
                    "2026-08-21",
                ],
                [
                    "2",
                    "-100",
                    "Food",
                    "Invalid",
                    "2026-08-21",
                ],
                [
                    "3",
                    "abc",
                    "Food",
                    "Invalid",
                    "2026-08-21",
                ],
                [
                    "4",
                    "300",
                    "",
                    "Invalid",
                    "2026-08-21",
                ],
                [
                    "5",
                    "200",
                    "Travel",
                    "Bus",
                    "invalid-date",
                ],
            ]
        )

        try:
            with patch(
                "builtins.input",
                return_value=csv_path
            ):
                main.import_expenses_from_csv()

            expenses = get_expenses()

            self.assertEqual(
                len(expenses),
                1
            )

            self.assertEqual(
                expenses[0][1],
                500
            )

        finally:
            os.remove(csv_path)

    def test_import_valid_csv(self):
        csv_path = self.create_csv_file(
            [
                [
                    "1",
                    "500",
                    "Food",
                    "Lunch",
                    "2026-08-21",
                ],
                [
                    "2",
                    "750",
                    "Travel",
                    "Bus",
                    "2026-08-22",
                ],
            ]
        )

        try:
            with patch(
                "builtins.input",
                return_value=csv_path
            ):
                main.import_expenses_from_csv()

            expenses = get_expenses()

            self.assertEqual(
                len(expenses),
                2
            )

            self.assertEqual(
                expenses[0][1],
                500
            )

            self.assertEqual(
                expenses[1][1],
                750
            )

        finally:
            os.remove(csv_path)

    def test_show_total_expenses(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.add_new_expense()

        main.show_total_expenses()

        self.assertEqual(
            database.get_total_expenses(),
            500
        )

    def test_show_category_totals(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.add_new_expense()

        main.show_category_totals()

        totals = dict(
            database.get_category_totals()
        )

        self.assertEqual(
            totals["Food"],
            500
        )

    def test_show_category_totals_empty(self):
        main.show_category_totals()

        self.assertEqual(
            database.get_category_totals(),
            []
        )

    def test_show_expenses_empty(self):
        main.view_expenses()

        self.assertEqual(
            get_expenses(),
            []
        )

    def test_show_expenses(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.add_new_expense()

        main.view_expenses()

        self.assertEqual(
            len(get_expenses()),
            1
        )

    def test_show_expense_statistics(self):
        with patch(
            "builtins.input",
            side_effect=[
                "500",
                "Food",
                "Lunch",
                "2026-08-21",
            ]
        ):
            main.add_new_expense()

        main.show_expense_statistics()

        statistics = database.get_expense_statistics()

        self.assertEqual(
            statistics["count"],
            1
        )

    def test_show_expense_statistics_empty(self):
        main.show_expense_statistics()

        statistics = database.get_expense_statistics()

        self.assertEqual(
            statistics["count"],
            0
        )

    def test_search_menu_back(self):
        with patch(
            "builtins.input",
            return_value="3"
        ):
            main.search_menu()

    def test_search_menu_invalid_choice(self):
        with patch(
            "builtins.input",
            side_effect=[
                "invalid",
                "3",
            ]
        ):
            main.search_menu()

    def test_main_exit(self):
        with patch(
            "builtins.input",
            return_value="14"
        ):
            main.main()


if __name__ == "__main__":
    unittest.main()