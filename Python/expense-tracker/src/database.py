import os
import sqlite3


DATABASE = os.getenv("EXPENSE_DB", "expenses.db")


def get_connection():
    return sqlite3.connect(DATABASE)


def create_table():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def add_expense(expense):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
        """,
        (
            expense.amount,
            expense.category,
            expense.description,
            expense.date,
        ),
    )

    connection.commit()
    connection.close()


def get_expenses():
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT id, amount, category, description, date
        FROM expenses
        ORDER BY id
        """
    )

    expenses = cursor.fetchall()

    connection.close()

    return expenses


def update_expense(expense_id, amount, category, description, date):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE expenses
        SET amount = ?, category = ?, description = ?, date = ?
        WHERE id = ?
        """,
        (
            amount,
            category,
            description,
            date,
            expense_id,
        ),
    )

    connection.commit()

    updated = cursor.rowcount

    connection.close()

    return updated


def delete_expense(expense_id):
    connection = get_connection()

    cursor = connection.execute(
        """
        DELETE FROM expenses
        WHERE id = ?
        """,
        (expense_id,),
    )

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    return deleted


def get_total_expenses():
    connection = get_connection()

    cursor = connection.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    )

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_category_totals():
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY category
        """
    )

    category_totals = cursor.fetchall()

    connection.close()

    return category_totals