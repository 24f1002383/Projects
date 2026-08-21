from database import add_expense, create_table, get_expenses
from expense import Expense


def add_new_expense():
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    description = input("Enter description: ")
    date = input("Enter date (YYYY-MM-DD): ")

    expense = Expense(
        amount,
        category,
        description,
        date,
    )

    add_expense(expense)
    print("Expense added successfully.")


def view_expenses():
    expenses = get_expenses()

    if not expenses:
        print("No expenses found.")
        return

    print("\n===== All Expenses =====")

    for expense in expenses:
        print(
            f"ID: {expense[0]} | "
            f"Amount: {expense[1]} | "
            f"Category: {expense[2]} | "
            f"Description: {expense[3]} | "
            f"Date: {expense[4]}"
        )


def main():
    create_table()

    while True:
        print("\n===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_new_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()