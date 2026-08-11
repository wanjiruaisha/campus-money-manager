import sqlite3


DATABASE_NAME = "campus_money.db"


def connect_db():
    """Create and return a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    """Create the required database tables if they do not exist."""

    conn = connect_db()
    cursor = conn.cursor()

    # Table for storing expenses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    # Table for storing budget information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            period TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_expense(expense):
    """Add a new expense to the database."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (
            amount,
            category,
            description,
            date
        )
        VALUES (?, ?, ?, ?)
    """, (
        expense.amount,
        expense.category,
        expense.description,
        expense.date
    ))

    conn.commit()

    # Get the ID SQLite created for the new expense
    expense.expense_id = cursor.lastrowid

    conn.close()

    return expense


def get_expenses():
    """Retrieve all expenses from the database."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, category, description, date
        FROM expenses
        ORDER BY id DESC
    """)

    expenses = cursor.fetchall()

    conn.close()

    return expenses


def update_expense(expense):
    """Update an existing expense."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE expenses
        SET amount = ?,
            category = ?,
            description = ?,
            date = ?
        WHERE id = ?
    """, (
        expense.amount,
        expense.category,
        expense.description,
        expense.date,
        expense.expense_id
    ))

    conn.commit()
    conn.close()


def delete_expense(expense_id):
    """Delete an expense using its ID."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()