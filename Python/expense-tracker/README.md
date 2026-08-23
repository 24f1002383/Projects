# 💰 Expense Tracker

A command-line expense tracker built with **Python** and **SQLite**.

This project was built to practice working with Python, SQLite, file handling, testing, and basic project structure. It can be used to keep track of daily expenses, manage a monthly budget, and generate simple expense reports — all from the terminal.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Menu](#-menu)
- [Expense Format](#-expense-format)
- [Budget Tracking](#-budget-tracking)
- [CSV Support](#-csv-support)
- [Statistics](#-statistics)
- [Testing](#-testing)
- [Database](#-database)
- [Git Workflow](#-git-workflow)
- [Future Plans](#-future-plans)
- [Author](#-author)

---

## ✨ Features

- Add, view, update and delete expenses
- Search expenses by category or date
- View total and category-wise expenses
- Get monthly expense summaries
- Set and track monthly budgets
- View expense statistics
- Export expenses to CSV
- Import expenses from CSV
- Basic input and date validation
- SQLite database for storing data
- Unit tests using Python's `unittest`

---

## 📁 Project Structure

```text
expense-tracker/
│
├── src/
│   ├── main.py
│   ├── database.py
│   └── expense.py
│
├── tests/
│   ├── test_database.py
│   └── test_main.py
│
├── README.md
└── .gitignore
```

> The SQLite database and generated CSV files are kept out of the repository using `.gitignore`.

---

## 🛠 Tech Stack

- Python
- SQLite (`sqlite3`)
- `unittest`
- `csv`

No third-party Python packages are required.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd expense-tracker
```

### 2. Check Python

Python 3.10+ is recommended.

```bash
python --version
```

### 3. Run the application

```bash
python src/main.py
```

The database is created automatically when the application starts.

---

## 📖 Menu

The application provides the following options:

```text
1.  Add Expense
2.  View Expenses
3.  Update Expense
4.  Delete Expense
5.  Total Expenses
6.  Category Summary
7.  Search Expenses
8.  Monthly Summary
9.  Set Monthly Budget
10. Budget Status
11. Expense Statistics
12. Export Expenses to CSV
13. Import Expenses from CSV
14. Exit
```

---

## 🧾 Expense Format

Each expense contains:

```text
Amount
Category
Description
Date
```

Dates use the `YYYY-MM-DD` format.

**Example:**

```text
500
Food
Lunch
2026-08-21
```

---

## 💵 Budget Tracking

A monthly budget can be set using the `YYYY-MM` format.

**Example:**

```text
Month:  2026-08
Budget: 10000
```

The application calculates the amount spent and the remaining budget for that month, and shows a warning when spending goes beyond the budget.

---

## 📤 CSV Support

Expenses can be exported to a CSV file for backup or further use.

**Example CSV structure:**

```text
ID,Amount,Category,Description,Date
1,500,Food,Lunch,2026-08-21
2,750,Travel,Bus,2026-08-22
```

CSV files can also be imported back into the application. Invalid rows are skipped instead of stopping the entire import.

> Generated CSV files are ignored by Git.

---

## 📊 Statistics

The statistics section currently shows:

- Total amount spent
- Number of expenses
- Average expense
- Highest expense
- Lowest expense

---

## 🧪 Testing

Tests are written using Python's built-in `unittest` framework.

Run all tests with:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

The tests cover:

- Database operations
- Budget functionality
- Expense statistics
- CSV import functionality

---

## 🗄 Database

SQLite is used as the database, so there is no separate database server to configure.

**Main tables:**

```text
expenses
budgets
```

The database file is created locally and is not committed to Git.

---

## 🔧 Git Workflow

Typical workflow for this project:

```bash
git status
git add .
git commit -m "Describe your changes"
git push
```

---

## 🔮 Future Plans

Some things that may be added later:

- [ ] Better command-line interface
- [ ] Expense charts and reports
- [ ] Recurring expenses
- [ ] More filtering options
- [ ] Yearly reports
- [ ] Better backup and restore support
- [ ] GUI version

---

## 👤 Author

**Krishna Kumar**
B.Tech CSE (AI & ML)
Government Engineering College, Samastipur

Built as a learning project while working with Python, SQLite, testing, and Git.