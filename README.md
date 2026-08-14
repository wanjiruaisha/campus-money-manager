# Campus Money Manager

Campus Money Manager is a desktop budgeting and expense management application designed to help students manage their money more effectively.

The application allows users to create accounts, set personal budgets, record expenses, track their remaining money, calculate a recommended daily allowance, and plan purchases before spending.

## Features

- User registration and login
- Secure password hashing and salting
- Separate budgets and expenses for each user
- Logout functionality
- Weekly and monthly budget management
- Add, view, edit, and delete expenses
- Expense categories such as Food, Transport, School, Printing, Airtime and Data, Entertainment, Personal Expenses, and Other
- Automatic calculation of total spending
- Remaining budget calculation
- Recommended daily allowance
- Budget progress tracking
- Recent expenses displayed on the dashboard
- Warning when an expense exceeds the remaining budget
- Purchase Planner to show how a planned purchase would affect the user's remaining budget and daily allowance
- Scrollable interfaces for smaller screens
- SQLite data persistence

## Technologies Used

- Python
- CustomTkinter
- Tkinter / ttk
- SQLite
- SQL
- Object-Oriented Programming
- Git and GitHub

## Project Structure

```text
campus-money-manager/
│
├── gui/
│   ├── __init__.py
│   ├── app.py
│   ├── auth.py
│   ├── dashboard.py
│   ├── expenses.py
│   ├── budget.py
│   └── affordability.py
│
├── main.py
├── database.py
├── models.py
├── utils.py
├── requirements.txt
├── README.md
└── .gitignore

## Installation

### 1. Clone the repository

```bash
git clone <https://github.com/wanjiruaisha/campus-money-manager.git>
```

Move into the project folder:

```bash
cd campus-money-manager
```

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
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

## Requirements

The `requirements.txt` file contains:

```text
customtkinter
```

The SQLite database file will be created automatically when the application runs.

## Main Sections

* **Dashboard** – Displays budget and spending information
* **Expenses** – Add, view, edit, and delete expenses
* **Budget** – Set or update a weekly or monthly budget

## Project Objective

The goal of Campus Money Manager is to help students manage limited amounts of money more effectively.

The application allows students to monitor their spending, set budgets, understand how much money they have remaining, and make more informed decisions before making purchases.

Instead of only recording expenses, the application also helps users understand how their spending affects the amount of money they can comfortably use each day.

## Future Improvements

* Expense search and filtering
* Spending charts
* CSV export
* Additional spending insights
* Budget history
* Spending category analysis
* More detailed financial insights

## Author

**Aisha Wanjiru**
