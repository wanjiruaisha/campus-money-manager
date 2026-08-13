import sqlite3
import hashlib
import secrets

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

    # authentication table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL
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

    cursor.execute(
        """
        INSERT INTO expenses (
            amount,
            category,
            description,
            date
        )
        VALUES (?, ?, ?, ?)
    """,
        (expense.amount, expense.category, expense.description, expense.date),
    )

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

    cursor.execute(
        """
        UPDATE expenses
        SET
            amount = ?,
            category = ?,
            description = ?,
            date = ?
        WHERE id = ?
    """,
        (
            expense.amount,
            expense.category,
            expense.description,
            expense.date,
            expense.expense_id,
        ),
    )

    conn.commit()
    conn.close()


def delete_expense(expense_id):
    """Delete an expense using its ID."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM expenses
        WHERE id = ?
    """,
        (expense_id,),
    )

    conn.commit()
    conn.close()


def get_recent_expenses(limit=5):
    """Return the most recent expenses."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            amount,
            category,
            description,
            date
        FROM expenses
        ORDER BY date DESC, id DESC
        LIMIT ?
    """,
        (limit,),
    )

    expenses = cursor.fetchall()

    conn.close()

    return expenses


def get_total_spent(start_date=None, end_date=None):
    """Calculate the total amount spent."""

    conn = connect_db()
    cursor = conn.cursor()

    if start_date and end_date:
        cursor.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE date BETWEEN ? AND ?
        """,
            (start_date, end_date),
        )

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
        cursor.execute(
            """
            UPDATE budget
            SET
                amount = ?,
                period = ?,
                start_date = ?,
                end_date = ?
            WHERE id = 1
        """,
            (budget.amount, budget.period, budget.start_date, budget.end_date),
        )

    else:
        cursor.execute(
            """
            INSERT INTO budget (
                id,
                amount,
                period,
                start_date,
                end_date
            )
            VALUES (1, ?, ?, ?, ?)
        """,
            (budget.amount, budget.period, budget.start_date, budget.end_date),
        )

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


def hash_password(password, salt):
    """Create a secure hash from a password and salt."""

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(salt),
        100000,
    )

    return password_hash.hex()


def create_user(username, password):
    """Create a new user account."""

    conn = connect_db()
    cursor = conn.cursor()

    # Check whether the username already exists
    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        (username,),
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return False, "Username already exists."

    # Create a random salt for this password
    salt = secrets.token_hex(16)

    # Hash the password
    password_hash = hash_password(
        password,
        salt,
    )

    # Save user
    cursor.execute(
        """
        INSERT INTO users (
            username,
            password_hash,
            salt
        )
        VALUES (?, ?, ?)
        """,
        (
            username,
            password_hash,
            salt,
        ),
    )

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    return True, user_id


def authenticate_user(username, password):
    """Check whether a username and password are correct."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, password_hash, salt
        FROM users
        WHERE username = ?
        """,
        (username,),
    )

    user = cursor.fetchone()

    conn.close()

    # Username does not exist
    if user is None:
        return None

    user_id, stored_username, stored_hash, salt = user

    # Hash the entered password using the stored salt
    entered_hash = hash_password(
        password,
        salt,
    )

    # Compare the hashes
    if entered_hash == stored_hash:
        return {
            "id": user_id,
            "username": stored_username,
        }

    return None
