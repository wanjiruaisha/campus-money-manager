import sqlite3


DATABASE_NAME = "campus_money.db"


def connect_db():
    """Create and return a connection to the database."""
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    """Create the required database tables."""

    conn = connect_db()
    cursor = conn.cursor()

    # Expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    # Budget table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY,
            amount REAL NOT NULL,
            period TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================
# EXPENSE FUNCTIONS
# =========================

def add_expense(expense):
    """Add a new expense."""

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

    expense.expense_id = cursor.lastrowid

    conn.close()

    return expense


def get_expenses():
    """Return all expenses."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            amount,
            category,
            description,
            date
        FROM expenses
        ORDER BY date DESC, id DESC
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
        SET
            amount = ?,
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

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (
        expense_id,
    ))

    conn.commit()
    conn.close()


def get_recent_expenses(limit=5):
    """Return the most recent expenses."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            amount,
            category,
            description,
            date
        FROM expenses
        ORDER BY date DESC, id DESC
        LIMIT ?
    """, (
        limit,
    ))

    expenses = cursor.fetchall()

    conn.close()

    return expenses


def get_total_spent(start_date=None, end_date=None):
    """Calculate the total amount spent."""

    conn = connect_db()
    cursor = conn.cursor()

    if start_date and end_date:
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE date BETWEEN ? AND ?
        """, (
            start_date,
            end_date
        ))

    else:
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
        """)

    total = cursor.fetchone()[0]

    conn.close()

    return float(total)


# =========================
# BUDGET FUNCTIONS
# =========================

def save_budget(budget):
    """Create or update the user's budget."""

    conn = connect_db()
    cursor = conn.cursor()

    # We only keep one current budget
    cursor.execute("""
        SELECT id
        FROM budget
        WHERE id = 1
    """)

    existing_budget = cursor.fetchone()

    if existing_budget:
        cursor.execute("""
            UPDATE budget
            SET
                amount = ?,
                period = ?,
                start_date = ?,
                end_date = ?
            WHERE id = 1
        """, (
            budget.amount,
            budget.period,
            budget.start_date,
            budget.end_date
        ))

    else:
        cursor.execute("""
            INSERT INTO budget (
                id,
                amount,
                period,
                start_date,
                end_date
            )
            VALUES (1, ?, ?, ?, ?)
        """, (
            budget.amount,
            budget.period,
            budget.start_date,
            budget.end_date
        ))

    conn.commit()
    conn.close()


def get_budget():
    """Return the current budget."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            amount,
            period,
            start_date,
            end_date
        FROM budget
        WHERE id = 1
    """)

    budget = cursor.fetchone()

    conn.close()

    return budget