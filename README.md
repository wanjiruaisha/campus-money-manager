# Campus Money Manager

Campus Money Manager is a desktop-based budgeting and expense management application built using Python, Tkinter, SQLite, and Object-Oriented Programming.

The application is designed to help students manage weekly or monthly budgets, record daily expenses, monitor spending, and make better decisions about how they use their available money.

## Features

* Set a weekly or monthly budget.
* Record daily expenses.
* Categorize expenses such as:

  * Food
  * Transport
  * School
  * Airtime and Data
  * Entertainment
  * Personal Expenses
* View previously recorded expenses.
* Edit existing expense records.
* Delete expense records.
* Automatically calculate total spending.
* Calculate the remaining budget.
* Calculate a recommended daily spending allowance.
* Check whether a planned purchase fits within the remaining budget.
* Store budget and expense information permanently using SQLite.

## Technologies Used

* **Python** – Main programming language and application logic.
* **Tkinter** – Used to build the graphical user interface.
* **SQLite** – Used to store budget and expense information.
* **SQL** – Used to create, retrieve, update, and delete database records.
* **Object-Oriented Programming (OOP)** – Used to organize the application using classes and objects.
* **Git & GitHub** – Used for version control and project management.

## Project Structure

```text
campus_money_manager/
│
├── main.py
├── gui.py
├── database.py
├── models.py
├── utils.py
├── README.md
└── .gitignore
```

### File Description

* `main.py` – Starts the application.
* `gui.py` – Contains the Tkinter graphical user interface.
* `database.py` – Handles SQLite database connections and CRUD operations.
* `models.py` – Contains OOP classes such as `Expense` and `Budget`.
* `utils.py` – Contains reusable calculations and helper functions.
* `README.md` – Contains project documentation.
* `.gitignore` – Specifies files that should not be tracked by Git.

## Database

The application uses SQLite as its local database.

The database stores:

* Expense amount
* Expense category
* Expense description
* Expense date
* Budget amount
* Budget period
* Budget start and end dates

The database supports CRUD operations:

* **Create** – Add new expenses and budgets.
* **Read** – View stored expenses and budget information.
* **Update** – Edit existing expense or budget records.
* **Delete** – Remove expense records.

## Getting Started

### Requirements

* Python 3
* Tkinter
* SQLite

Tkinter and SQLite are included with most standard Python installations.

### Running the Application

Clone or download the project, open the project folder in a terminal, and run:

```bash
python main.py
```

## Project Objective

The main objective of Campus Money Manager is to create a simple desktop application that helps students monitor and manage limited weekly or monthly funds while demonstrating the practical use of Python, Tkinter, SQLite, SQL, CRUD operations, and Object-Oriented Programming.

## Future Improvements

Possible future improvements include:

* Expense search and filtering.
* Spending charts and visual reports.
* Emergency savings management.
* Exporting expense reports to CSV.
* More detailed spending insights.

## Author

**Aisha Wanjiru**
