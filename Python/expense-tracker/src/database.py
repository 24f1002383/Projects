import os
import sqlite3
from contextlib import contextmanager


DATABASE = os.getenv("EXPENSE_DB", "expenses.db")


@contextmanager
def database_connection():
    connection = sqlite3.connect(DATABASE)

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def create_table():
    with database_connection() as connection:
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

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month TEXT NOT NULL UNIQUE,
                amount REAL NOT NULL
            )
            """
        )


def add_expense(expense):
    with database_connection() as connection:
        connection.execute(
            """
            INSERT INTO expenses
                (amount, category, description, date)
            VALUES (?, ?, ?, ?)
            """,
            (
                expense.amount,
                expense.category,
                expense.description,
                expense.date,
            ),
        )


def get_expenses():
    with database_connection() as connection:
        cursor = connection.execute(
            """
            SELECT id, amount, category, description, date
            FROM expenses
            ORDER BY id
            """
        )

        return cursor.fetchall()


def update_expense(
    expense_id,
    amount,
    category,
    description,
    date,
):
    with database_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE expenses
            SET amount = ?,
                category = ?,
                description = ?,
                date = ?
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

        return cursor.rowcount


def delete_expense(expense_id):
    with database_connection() as connection:
        cursor = connection.execute(
            """
            DELETE FROM expenses
            WHERE id = ?
            """,
            (expense_id,),
        )

        return cursor.rowcount


def get_total_expenses():
    with database_connection() as connection:
        cursor = connection.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            """
        )

        return cursor.fetchone()[0]


def get_category_totals():
    with database_connection() as connection:
        cursor = connection.execute(
            """
            SELECT category, SUM(amount)
            FROM expenses
            GROUP BY category
            ORDER BY category
            """
        )

        return cursor.fetchall()


def search_expenses(category):
    with database_connection() as connection:
        cursor = connection.execute(
            """
            SELECT id, amount, category, description, date
            FROM expenses
            WHERE LOWER(category) = LOWER(?)
            ORDER BY id
            """,
            (category,),
        )

        return cursor.fetchall()


def search_expenses_by_date(date):
    with database_connection() as connection:
        cursor = connection.execute(
            """
            SELECT id, amount, category, description, date
            FROM expenses
            WHERE date = ?
            ORDER BY id
            """,
            (date,),
        )

        return cursor.fetchall()


def get_monthly_summary(month):
    with database_connection() as connection:
        cursor = connection.execute(
            """
            SELECT category, SUM(amount)
            FROM expenses
            WHERE substr(date, 1, 7) = ?
            GROUP BY category
            ORDER BY category
            """,
            (month,),
        )

        return cursor.fetchall()


def get_monthly_total(month):
    with database_connection() as connection:
        cursor = connection.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE substr(date, 1, 7) = ?
            """,
            (month,),
        )

        return cursor.fetchone()[0]


def set_monthly_budget(month, amount):
    with database_connection() as connection:
        connection.execute(
            """
            INSERT INTO budgets (month, amount)
            VALUES (?, ?)
            ON CONFLICT(month)
            DO UPDATE SET amount = excluded.amount
            """,
            (month, amount),
        )


def get_monthly_budget(month):
    with database_connection() as connection:
        cursor = connection.execute(
            """
            SELECT amount
            FROM budgets
            WHERE month = ?
            """,
            (month,),
        )

        result = cursor.fetchone()

        if result is None:
            return None

        return result[0]


def get_budget_status(month):
    budget = get_monthly_budget(month)
    spent = get_monthly_total(month)

    if budget is None:
        return None

    return {
        "budget": budget,
        "spent": spent,
        "remaining": budget - spent,
    }


def get_expense_statistics():
    with database_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                COUNT(*),
                COALESCE(SUM(amount), 0),
                COALESCE(AVG(amount), 0),
                COALESCE(MAX(amount), 0),
                COALESCE(MIN(amount), 0)
            FROM expenses
            """
        )

        result = cursor.fetchone()

        return {
            "count": result[0],
            "total": result[1],
            "average": result[2],
            "highest": result[3],
            "lowest": result[4],
        }