import sqlite3

DATABASE = "expenses.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

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