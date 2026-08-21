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
from database import (
    create_table,
    add_expense,
    get_expenses,
    update_expense,
    delete_expense,
    get_total_expenses,
    get_category_totals,
)
from expense import Expense


class TestDatabase(unittest.TestCase):

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

    def test_add_expense(self):
        expense = Expense(
            500,
            "Food",
            "Lunch",
            "2026-08-21"
        )

        add_expense(expense)

        expenses = get_expenses()

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0][1], 500)
        self.assertEqual(expenses[0][2], "Food")
        self.assertEqual(expenses[0][3], "Lunch")
        self.assertEqual(expenses[0][4], "2026-08-21")

    def test_get_expenses(self):
        expense1 = Expense(
            500,
            "Food",
            "Lunch",
            "2026-08-21"
        )

        expense2 = Expense(
            750,
            "Travel",
            "Bus ticket",
            "2026-08-21"
        )

        add_expense(expense1)
        add_expense(expense2)

        expenses = get_expenses()

        self.assertEqual(len(expenses), 2)

    def test_update_expense(self):
        expense = Expense(
            1000,
            "Shopping",
            "Shoes",
            "2026-08-21"
        )

        add_expense(expense)

        expenses = get_expenses()
        expense_id = expenses[0][0]

        update_expense(
            expense_id,
            1200,
            "Shopping",
            "New shoes",
            "2026-08-22"
        )

        updated_expenses = get_expenses()

        self.assertEqual(updated_expenses[0][1], 1200)
        self.assertEqual(updated_expenses[0][3], "New shoes")
        self.assertEqual(updated_expenses[0][4], "2026-08-22")

    def test_delete_expense(self):
        expense = Expense(
            300,
            "Food",
            "Snacks",
            "2026-08-21"
        )

        add_expense(expense)

        expenses = get_expenses()
        expense_id = expenses[0][0]

        delete_expense(expense_id)

        expenses = get_expenses()

        self.assertEqual(len(expenses), 0)

    def test_total_expenses(self):
        expense1 = Expense(
            400,
            "Food",
            "Breakfast",
            "2026-08-21"
        )

        expense2 = Expense(
            600,
            "Travel",
            "Bus",
            "2026-08-21"
        )

        add_expense(expense1)
        add_expense(expense2)

        total = get_total_expenses()

        self.assertEqual(total, 1000)

    def test_category_totals(self):
        expense1 = Expense(
            200,
            "Food",
            "Breakfast",
            "2026-08-21"
        )

        expense2 = Expense(
            300,
            "Food",
            "Lunch",
            "2026-08-21"
        )

        expense3 = Expense(
            500,
            "Travel",
            "Bus",
            "2026-08-21"
        )

        add_expense(expense1)
        add_expense(expense2)
        add_expense(expense3)

        category_totals = dict(get_category_totals())

        self.assertEqual(category_totals["Food"], 500)
        self.assertEqual(category_totals["Travel"], 500)


if __name__ == "__main__":
    unittest.main()