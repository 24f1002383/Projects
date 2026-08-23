import os
import sqlite3


DATABASE = os.getenv("EXPENSE_DB", "expenses.db")


def get_connection():
    return sqlite3.connect(DATABASE)


def create_table():
    connection = get_connection()

    try:
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

        connection.commit()
    finally:
        connection.close()


def add_expense(expense):
    connection = get_connection()

    try:
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

        connection.commit()
    finally:
        connection.close()


def get_expenses():
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT id, amount, category, description, date
            FROM expenses
            ORDER BY id
            """
        )

        return cursor.fetchall()
    finally:
        connection.close()


def update_expense(
    expense_id,
    amount,
    category,
    description,
    date,
):
    connection = get_connection()

    try:
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

        return cursor.rowcount
    finally:
        connection.close()


def delete_expense(expense_id):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM expenses
            WHERE id = ?
            """,
            (expense_id,),
        )

        connection.commit()

        return cursor.rowcount
    finally:
        connection.close()


def get_total_expenses():
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            """
        )

        return cursor.fetchone()[0]
    finally:
        connection.close()


def get_category_totals():
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT category, SUM(amount)
            FROM expenses
            GROUP BY category
            ORDER BY category
            """
        )

        return cursor.fetchall()
    finally:
        connection.close()


def search_expenses(category):
    connection = get_connection()

    try:
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
    finally:
        connection.close()


def search_expenses_by_date(date):
    connection = get_connection()

    try:
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
    finally:
        connection.close()


def get_monthly_summary(month):
    connection = get_connection()

    try:
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
    finally:
        connection.close()


def get_monthly_total(month):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE substr(date, 1, 7) = ?
            """,
            (month,),
        )

        return cursor.fetchone()[0]
    finally:
        connection.close()


def set_monthly_budget(month, amount):
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO budgets (month, amount)
            VALUES (?, ?)
            ON CONFLICT(month)
            DO UPDATE SET amount = excluded.amount
            """,
            (month, amount),
        )

        connection.commit()
    finally:
        connection.close()


def get_monthly_budget(month):
    connection = get_connection()

    try:
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
    finally:
        connection.close()


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
    connection = get_connection()

    try:
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
    finally:
        connection.close()