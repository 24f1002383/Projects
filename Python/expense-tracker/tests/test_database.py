import os
import sys
import tempfile
import unittest

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../src")
    )
)

import database

from expense import Expense


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.test_db = tempfile.NamedTemporaryFile(
            suffix=".db",
            delete=False
        )

        self.test_db.close()

        database.DATABASE = self.test_db.name

        database.create_table()

    def tearDown(self):
        if os.path.exists(self.test_db.name):
            os.remove(self.test_db.name)

    def add_sample_expense(
        self,
        amount=500,
        category="Food",
        description="Lunch",
        date="2026-08-21",
    ):
        expense = Expense(
            amount,
            category,
            description,
            date,
        )

        database.add_expense(expense)

    def test_create_table(self):
        connection = database.get_connection()

        cursor = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        )

        tables = {
            row[0]
            for row in cursor.fetchall()
        }

        connection.close()

        self.assertIn("expenses", tables)
        self.assertIn("budgets", tables)

    def test_add_expense(self):
        self.add_sample_expense()

        expenses = database.get_expenses()

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0][1], 500)
        self.assertEqual(expenses[0][2], "Food")
        self.assertEqual(expenses[0][3], "Lunch")
        self.assertEqual(expenses[0][4], "2026-08-21")

    def test_get_expenses(self):
        self.add_sample_expense(
            500,
            "Food",
            "Lunch",
            "2026-08-21",
        )

        self.add_sample_expense(
            750,
            "Travel",
            "Bus",
            "2026-08-22",
        )

        expenses = database.get_expenses()

        self.assertEqual(len(expenses), 2)

    def test_update_expense(self):
        self.add_sample_expense()

        updated = database.update_expense(
            1,
            750,
            "Travel",
            "Bus",
            "2026-08-22",
        )

        self.assertEqual(updated, 1)

        expenses = database.get_expenses()

        self.assertEqual(expenses[0][1], 750)
        self.assertEqual(expenses[0][2], "Travel")
        self.assertEqual(expenses[0][3], "Bus")
        self.assertEqual(expenses[0][4], "2026-08-22")

    def test_update_non_existing_expense(self):
        updated = database.update_expense(
            999,
            500,
            "Food",
            "Lunch",
            "2026-08-21",
        )

        self.assertEqual(updated, 0)

    def test_delete_expense(self):
        self.add_sample_expense()

        deleted = database.delete_expense(1)

        self.assertEqual(deleted, 1)
        self.assertEqual(
            len(database.get_expenses()),
            0
        )

    def test_delete_non_existing_expense(self):
        deleted = database.delete_expense(999)

        self.assertEqual(deleted, 0)

    def test_get_total_expenses_empty(self):
        total = database.get_total_expenses()

        self.assertEqual(total, 0)

    def test_get_total_expenses(self):
        self.add_sample_expense(
            500,
            "Food",
            "Lunch",
            "2026-08-21",
        )

        self.add_sample_expense(
            750,
            "Travel",
            "Bus",
            "2026-08-22",
        )

        total = database.get_total_expenses()

        self.assertEqual(total, 1250)

    def test_get_category_totals(self):
        self.add_sample_expense(
            500,
            "Food",
            "Lunch",
            "2026-08-21",
        )

        self.add_sample_expense(
            300,
            "Food",
            "Dinner",
            "2026-08-22",
        )

        self.add_sample_expense(
            700,
            "Travel",
            "Bus",
            "2026-08-23",
        )

        totals = dict(
            database.get_category_totals()
        )

        self.assertEqual(totals["Food"], 800)
        self.assertEqual(totals["Travel"], 700)

    def test_search_expenses(self):
        self.add_sample_expense(
            500,
            "Food",
            "Lunch",
            "2026-08-21",
        )

        self.add_sample_expense(
            700,
            "Travel",
            "Bus",
            "2026-08-22",
        )

        expenses = database.search_expenses("Food")

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0][2], "Food")

    def test_search_expenses_case_insensitive(self):
        self.add_sample_expense(
            500,
            "Food",
            "Lunch",
            "2026-08-21",
        )

        expenses = database.search_expenses("food")

        self.assertEqual(len(expenses), 1)

    def test_search_expenses_no_result(self):
        expenses = database.search_expenses("Travel")

        self.assertEqual(len(expenses), 0)

    def test_search_expenses_by_date(self):
        self.add_sample_expense(
            500,
            "Food",
            "Lunch",
            "2026-08-21",
        )

        self.add_sample_expense(
            700,
            "Travel",
            "Bus",
            "2026-08-22",
        )

        expenses = database.search_expenses_by_date(
            "2026-08-21"
        )

        self.assertEqual(len(expenses), 1)
        self.assertEqual(
            expenses[0][4],
            "2026-08-21"
        )

    def test_search_expenses_by_date_no_result(self):
        expenses = database.search_expenses_by_date(
            "2026-08-30"
        )

        self.assertEqual(len(expenses), 0)

    def test_monthly_total(self):
        self.add_sample_expense(
            500,
            "Food",
            "Lunch",
            "2026-08-21",
        )

        self.add_sample_expense(
            700,
            "Travel",
            "Bus",
            "2026-08-22",
        )

        self.add_sample_expense(
            300,
            "Food",
            "Dinner",
            "2026-09-01",
        )

        total = database.get_monthly_total(
            "2026-08"
        )

        self.assertEqual(total, 1200)

    def test_monthly_total_empty(self):
        total = database.get_monthly_total(
            "2026-08"
        )

        self.assertEqual(total, 0)

    def test_monthly_summary(self):
        self.add_sample_expense(
            500,
            "Food",
            "Lunch",
            "2026-08-21",
        )

        self.add_sample_expense(
            300,
            "Food",
            "Dinner",
            "2026-08-22",
        )

        self.add_sample_expense(
            700,
            "Travel",
            "Bus",
            "2026-08-23",
        )

        summary = dict(
            database.get_monthly_summary("2026-08")
        )

        self.assertEqual(summary["Food"], 800)
        self.assertEqual(summary["Travel"], 700)

    def test_monthly_summary_empty(self):
        summary = database.get_monthly_summary(
            "2026-08"
        )

        self.assertEqual(summary, [])

    def test_set_monthly_budget(self):
        database.set_monthly_budget(
            "2026-08",
            5000,
        )

        budget = database.get_monthly_budget(
            "2026-08"
        )

        self.assertEqual(budget, 5000)

    def test_update_monthly_budget(self):
        database.set_monthly_budget(
            "2026-08",
            5000,
        )

        database.set_monthly_budget(
            "2026-08",
            7000,
        )

        budget = database.get_monthly_budget(
            "2026-08"
        )

        self.assertEqual(budget, 7000)

    def test_get_monthly_budget_not_found(self):
        budget = database.get_monthly_budget(
            "2026-08"
        )

        self.assertIsNone(budget)

    def test_get_budget_status(self):
        self.add_sample_expense(
            1000,
            "Food",
            "Lunch",
            "2026-08-21",
        )

        database.set_monthly_budget(
            "2026-08",
            5000,
        )

        status = database.get_budget_status(
            "2026-08"
        )

        self.assertEqual(status["budget"], 5000)
        self.assertEqual(status["spent"], 1000)
        self.assertEqual(status["remaining"], 4000)

    def test_get_budget_status_without_budget(self):
        status = database.get_budget_status(
            "2026-08"
        )

        self.assertIsNone(status)

    def test_expense_statistics_empty(self):
        statistics = database.get_expense_statistics()

        self.assertEqual(statistics["count"], 0)
        self.assertEqual(statistics["total"], 0)
        self.assertEqual(statistics["average"], 0)
        self.assertEqual(statistics["highest"], 0)
        self.assertEqual(statistics["lowest"], 0)

    def test_expense_statistics(self):
        self.add_sample_expense(
            500,
            "Food",
            "Lunch",
            "2026-08-21",
        )

        self.add_sample_expense(
            1000,
            "Travel",
            "Bus",
            "2026-08-22",
        )

        self.add_sample_expense(
            1500,
            "Shopping",
            "Clothes",
            "2026-08-23",
        )

        statistics = database.get_expense_statistics()

        self.assertEqual(
            statistics["count"],
            3
        )

        self.assertEqual(
            statistics["total"],
            3000
        )

        self.assertEqual(
            statistics["average"],
            1000
        )

        self.assertEqual(
            statistics["highest"],
            1500
        )

        self.assertEqual(
            statistics["lowest"],
            500
        )


if __name__ == "__main__":
    unittest.main()