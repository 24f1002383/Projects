import os
import sys
import unittest

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../src")
    )
)

from expense import Expense


class TestExpense(unittest.TestCase):

    def test_expense_creation(self):
        expense = Expense(
            500,
            "Food",
            "Lunch",
            "2026-08-21",
        )

        self.assertEqual(expense.amount, 500)
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.description, "Lunch")
        self.assertEqual(expense.date, "2026-08-21")

    def test_expense_string(self):
        expense = Expense(
            500,
            "Food",
            "Lunch",
            "2026-08-21",
        )

        result = str(expense)

        self.assertIn("Amount: 500", result)
        self.assertIn("Category: Food", result)
        self.assertIn("Description: Lunch", result)
        self.assertIn("Date: 2026-08-21", result)

    def test_expense_with_decimal_amount(self):
        expense = Expense(
            499.50,
            "Travel",
            "Bus ticket",
            "2026-08-22",
        )

        self.assertEqual(
            expense.amount,
            499.50
        )

    def test_expense_with_empty_description(self):
        expense = Expense(
            100,
            "Food",
            "",
            "2026-08-21",
        )

        self.assertEqual(
            expense.description,
            ""
        )


if __name__ == "__main__":
    unittest.main()