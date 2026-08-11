# Campus Money Manager

Campus Money Manager is a desktop budgeting and expense management application built using Python, Tkinter, SQLite, and Object-Oriented Programming.

It is designed to help students manage weekly or monthly budgets, record daily expenses, monitor spending, and make better financial decisions.

## Features

* Set a weekly or monthly budget
* Add daily expenses
* Categorize expenses
* View expense history
* Edit expenses
* Delete expenses
* Calculate total spending
* Calculate remaining budget
* Calculate recommended daily allowance
* Check whether a planned purchase fits within the remaining budget
* Store data permanently using SQLite

## Technologies Used

* Python
* Tkinter
* SQLite
* SQL
* Object-Oriented Programming
* Git & GitHub

## Project Structure

```text
campus-money-manager/
│
├── gui/
│   ├── __init__.py
│   ├── app.py
│   ├── dashboard.py
│   ├── expenses.py
│   ├── budget.py
│   └── affordability.py
│
├── main.py
├── database.py
├── models.py
├── utils.py
├── README.md
└── .gitignore
```

## Installation

### 1. Clone the repository

```bash
git clone <https://github.com/wanjiruaisha/campus-money-manager.git>
```

Move into the project folder:

```bash
cd campus-money-manager
```

### 2. Check Python

Make sure Python 3 is installed:

```bash
python --version
```

### 3. Check Tkinter

Tkinter normally comes with Python.

```bash
python -m tkinter
```

A small Tkinter window should open.

SQLite is also included with Python, so no additional installation is required.

## Run the Application

From inside the project folder:

```bash
python main.py
```

The SQLite database file will be created automatically when the application runs.

## Main Sections

* **Dashboard** – Displays budget and spending information
* **Expenses** – Add, view, edit, and delete expenses
* **Budget** – Set or update a weekly or monthly budget
* **Can I Afford This?** – Check whether a planned purchase fits within the remaining budget

## Project Objective

The objective of this project is to build a student budgeting application while demonstrating Python, Tkinter, SQLite, SQL, CRUD operations, OOP, input validation, and modular programming.

## Future Improvements

* Expense search and filtering
* Spending charts
* CSV export
* Additional spending insights

## Author

**Aisha Wanjiru**
