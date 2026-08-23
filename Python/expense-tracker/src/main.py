import csv
from datetime import datetime

from database import (
    add_expense,
    create_table,
    delete_expense,
    get_budget_status,
    get_category_totals,
    get_expense_statistics,
    get_expenses,
    get_monthly_summary,
    get_monthly_total,
    get_total_expenses,
    search_expenses,
    search_expenses_by_date,
    set_monthly_budget,
    update_expense,
)
from expense import Expense


def validate_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return len(date) == 10 and date[4] == "-" and date[7] == "-"
    except ValueError:
        return False


def validate_month(month):
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        return False

    return len(month) == 7 and month[4] == "-"


def add_new_expense():
    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        category = input("Enter category: ").strip()
        description = input("Enter description: ").strip()
        date = input("Enter date (YYYY-MM-DD): ").strip()

        if not category:
            print("Category cannot be empty.")
            return

        if not validate_date(date):
            print("Invalid date format. Use YYYY-MM-DD.")
            return

        expense = Expense(
            amount,
            category,
            description,
            date,
        )

        add_expense(expense)

        print("Expense added successfully.")

    except ValueError:
        print("Please enter a valid amount.")


def view_expenses():
    expenses = get_expenses()

    if not expenses:
        print("No expenses found.")
        return

    print("\n===== All Expenses =====")

    for expense in expenses:
        print(
            f"ID: {expense[0]} | "
            f"Amount: {expense[1]:.2f} | "
            f"Category: {expense[2]} | "
            f"Description: {expense[3]} | "
            f"Date: {expense[4]}"
        )


def update_existing_expense():
    try:
        expense_id = int(input("Enter expense ID: "))
        amount = float(input("Enter new amount: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        category = input("Enter new category: ").strip()
        description = input("Enter new description: ").strip()
        date = input("Enter new date (YYYY-MM-DD): ").strip()

        if not category:
            print("Category cannot be empty.")
            return

        if not validate_date(date):
            print("Invalid date format. Use YYYY-MM-DD.")
            return

        updated = update_expense(
            expense_id,
            amount,
            category,
            description,
            date,
        )

        if updated:
            print("Expense updated successfully.")
        else:
            print("Expense not found.")

    except ValueError:
        print("Please enter valid values.")


def delete_existing_expense():
    try:
        expense_id = int(input("Enter expense ID: "))

        deleted = delete_expense(expense_id)

        if deleted:
            print("Expense deleted successfully.")
        else:
            print("Expense not found.")

    except ValueError:
        print("Please enter a valid expense ID.")


def show_total_expenses():
    total = get_total_expenses()

    print(f"\nTotal Expenses: {total:.2f}")


def show_category_totals():
    category_totals = get_category_totals()

    if not category_totals:
        print("No expenses found.")
        return

    print("\n===== Category Summary =====")

    for category, total in category_totals:
        print(f"{category}: {total:.2f}")


def search_existing_expenses():
    category = input("Enter category to search: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    expenses = search_expenses(category)

    if not expenses:
        print("No expenses found.")
        return

    print("\n===== Search Results =====")

    for expense in expenses:
        print(
            f"ID: {expense[0]} | "
            f"Amount: {expense[1]:.2f} | "
            f"Category: {expense[2]} | "
            f"Description: {expense[3]} | "
            f"Date: {expense[4]}"
        )


def search_expenses_by_date_menu():
    date = input("Enter date (YYYY-MM-DD): ").strip()

    if not validate_date(date):
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    expenses = search_expenses_by_date(date)

    if not expenses:
        print("No expenses found.")
        return

    print("\n===== Date Search Results =====")

    for expense in expenses:
        print(
            f"ID: {expense[0]} | "
            f"Amount: {expense[1]:.2f} | "
            f"Category: {expense[2]} | "
            f"Description: {expense[3]} | "
            f"Date: {expense[4]}"
        )


def search_menu():
    while True:
        print("\n===== Search Expenses =====")
        print("1. Search by Category")
        print("2. Search by Date")
        print("3. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            search_existing_expenses()

        elif choice == "2":
            search_expenses_by_date_menu()

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please try again.")


def show_monthly_summary():
    month = input("Enter month (YYYY-MM): ").strip()

    if not validate_month(month):
        print("Invalid month format. Use YYYY-MM.")
        return

    total = get_monthly_total(month)
    summary = get_monthly_summary(month)

    if not summary:
        print("No expenses found for this month.")
        return

    print(f"\n===== Monthly Summary: {month} =====")
    print(f"Total Expenses: {total:.2f}")

    print("\nCategory-wise:")

    for category, amount in summary:
        print(f"{category}: {amount:.2f}")


def set_budget():
    month = input("Enter month (YYYY-MM): ").strip()

    if not validate_month(month):
        print("Invalid month format. Use YYYY-MM.")
        return

    try:
        amount = float(input("Enter monthly budget: "))

        if amount <= 0:
            print("Budget must be greater than zero.")
            return

        set_monthly_budget(month, amount)

        print("Monthly budget saved successfully.")

    except ValueError:
        print("Please enter a valid amount.")


def show_budget_status():
    month = input("Enter month (YYYY-MM): ").strip()

    if not validate_month(month):
        print("Invalid month format. Use YYYY-MM.")
        return

    status = get_budget_status(month)

    if status is None:
        print("No budget set for this month.")
        return

    print(f"\n===== Budget Status: {month} =====")
    print(f"Budget: {status['budget']:.2f}")
    print(f"Spent: {status['spent']:.2f}")
    print(f"Remaining: {status['remaining']:.2f}")

    if status["remaining"] < 0:
        print("Warning: You have exceeded your monthly budget.")


def show_expense_statistics():
    statistics = get_expense_statistics()

    if statistics["count"] == 0:
        print("No expenses found.")
        return

    print("\n===== Expense Statistics =====")
    print(f"Total Expenses: {statistics['total']:.2f}")
    print(f"Number of Expenses: {statistics['count']}")
    print(f"Average Expense: {statistics['average']:.2f}")
    print(f"Highest Expense: {statistics['highest']:.2f}")
    print(f"Lowest Expense: {statistics['lowest']:.2f}")


def export_expenses_to_csv():
    expenses = get_expenses()

    if not expenses:
        print("No expenses found.")
        return

    filename = input(
        "Enter CSV filename (default: expenses.csv): "
    ).strip()

    if not filename:
        filename = "expenses.csv"

    if not filename.endswith(".csv"):
        filename += ".csv"

    try:
        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.writer(file)

            writer.writerow(
                [
                    "ID",
                    "Amount",
                    "Category",
                    "Description",
                    "Date",
                ]
            )

            writer.writerows(expenses)

        print(
            f"Expenses exported successfully to {filename}."
        )

    except OSError as error:
        print(f"Unable to export expenses: {error}")


def import_expenses_from_csv():
    filename = input("Enter CSV filename: ").strip()

    if not filename:
        print("Filename cannot be empty.")
        return

    try:
        with open(
            filename,
            "r",
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            required_columns = {
                "ID",
                "Amount",
                "Category",
                "Description",
                "Date",
            }

            if not reader.fieldnames:
                print("CSV file is empty or invalid.")
                return

            if not required_columns.issubset(
                reader.fieldnames
            ):
                print("Invalid CSV format.")
                return

            imported = 0
            skipped = 0

            for row in reader:
                try:
                    amount = float(row["Amount"])
                    category = row["Category"].strip()
                    description = row["Description"].strip()
                    date = row["Date"].strip()

                    if amount <= 0:
                        skipped += 1
                        continue

                    if not category:
                        skipped += 1
                        continue

                    if not validate_date(date):
                        skipped += 1
                        continue

                    expense = Expense(
                        amount,
                        category,
                        description,
                        date,
                    )

                    add_expense(expense)
                    imported += 1

                except (ValueError, TypeError):
                    skipped += 1

        print(f"Imported expenses: {imported}")
        print(f"Skipped rows: {skipped}")

    except FileNotFoundError:
        print("CSV file not found.")

    except OSError as error:
        print(f"Unable to read CSV file: {error}")


def main():
    create_table()

    while True:
        print("\n===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Total Expenses")
        print("6. Category Summary")
        print("7. Search Expenses")
        print("8. Monthly Summary")
        print("9. Set Monthly Budget")
        print("10. Budget Status")
        print("11. Expense Statistics")
        print("12. Export Expenses to CSV")
        print("13. Import Expenses from CSV")
        print("14. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_new_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            update_existing_expense()

        elif choice == "4":
            delete_existing_expense()

        elif choice == "5":
            show_total_expenses()

        elif choice == "6":
            show_category_totals()

        elif choice == "7":
            search_menu()

        elif choice == "8":
            show_monthly_summary()

        elif choice == "9":
            set_budget()

        elif choice == "10":
            show_budget_status()

        elif choice == "11":
            show_expense_statistics()

        elif choice == "12":
            export_expenses_to_csv()

        elif choice == "13":
            import_expenses_from_csv()

        elif choice == "14":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()