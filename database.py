import hashlib
import secrets
import sqlite3

DATABASE_NAME = "campus_money.db"

# Stores the ID of the user who is currently logged in
CURRENT_USER_ID = None


def connect_db():
    """Create and return a connection to the database."""

    conn = sqlite3.connect(DATABASE_NAME)

    # Turn on foreign key support
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# =========================
# CURRENT USER
# =========================


def set_current_user(user_id):
    """Store the currently logged-in user's ID."""

    global CURRENT_USER_ID
    CURRENT_USER_ID = user_id


def get_current_user_id():
    """Return the currently logged-in user's ID."""

    if CURRENT_USER_ID is None:
        raise ValueError("No user is currently logged in.")

    return CURRENT_USER_ID


# =========================
# CREATE TABLES
# =========================


def create_tables():
    """Create all required database tables."""

    conn = connect_db()
    cursor = conn.cursor()

    # -------------------------
    # USERS
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
        """)

    # -------------------------
    # EXPENSES
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        )
        """)

    # -------------------------
    # BUDGET
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            amount REAL NOT NULL,
            period TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        )
        """)

    conn.commit()
    conn.close()


# =========================
# PASSWORD FUNCTIONS
# =========================


def hash_password(password, salt):
    """Create a hash from a password and salt."""

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(salt),
        200000,
    )

    return password_hash.hex()


# =========================
# USER AUTHENTICATION
# =========================


def create_user(username, password):
    """Create a new user account."""

    conn = connect_db()
    cursor = conn.cursor()

    # Check whether username already exists
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

        return (
            False,
            "Username already exists.",
        )

    # Generate a random salt
    salt = secrets.token_hex(16)

    # Hash password before storing it
    password_hash = hash_password(
        password,
        salt,
    )

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
    """Check whether login details are correct."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            password_hash,
            salt
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

    (
        user_id,
        stored_username,
        stored_hash,
        salt,
    ) = user

    # Hash the password entered during login
    entered_hash = hash_password(
        password,
        salt,
    )

    # Compare it with the stored password hash
    if entered_hash == stored_hash:
        return {
            "id": user_id,
            "username": stored_username,
        }

    return None


# =========================
# EXPENSE - CREATE
# =========================


def add_expense(expense):
    """Add an expense for the logged-in user."""

    user_id = get_current_user_id()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO expenses (
            user_id,
            amount,
            category,
            description,
            date
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            expense.amount,
            expense.category,
            expense.description,
            expense.date,
        ),
    )

    conn.commit()

    expense.expense_id = cursor.lastrowid

    conn.close()

    return expense


# =========================
# EXPENSE - READ
# =========================


def get_expenses():
    """Get expenses belonging to the logged-in user."""

    user_id = get_current_user_id()

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
        WHERE user_id = ?
        ORDER BY date DESC, id DESC
        """,
        (user_id,),
    )

    expenses = cursor.fetchall()

    conn.close()

    return expenses


# =========================
# EXPENSE - UPDATE
# =========================


def update_expense(expense):
    """Update an expense belonging to the logged-in user."""

    user_id = get_current_user_id()

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
        AND user_id = ?
        """,
        (
            expense.amount,
            expense.category,
            expense.description,
            expense.date,
            expense.expense_id,
            user_id,
        ),
    )

    conn.commit()
    conn.close()


# =========================
# EXPENSE - DELETE
# =========================


def delete_expense(expense_id):
    """Delete an expense belonging to the logged-in user."""

    user_id = get_current_user_id()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM expenses

        WHERE id = ?
        AND user_id = ?
        """,
        (
            expense_id,
            user_id,
        ),
    )

    conn.commit()
    conn.close()


# =========================
# RECENT EXPENSES
# =========================


def get_recent_expenses(limit=5):
    """Get recent expenses for the logged-in user."""

    user_id = get_current_user_id()

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

        WHERE user_id = ?

        ORDER BY date DESC, id DESC

        LIMIT ?
        """,
        (
            user_id,
            limit,
        ),
    )

    expenses = cursor.fetchall()

    conn.close()

    return expenses


# =========================
# TOTAL SPENT
# =========================


def get_total_spent(
    start_date=None,
    end_date=None,
):
    """Calculate spending for the logged-in user."""

    user_id = get_current_user_id()

    conn = connect_db()
    cursor = conn.cursor()

    # Calculate spending within a budget period
    if start_date and end_date:

        cursor.execute(
            """
            SELECT COALESCE(
                SUM(amount),
                0
            )

            FROM expenses

            WHERE user_id = ?
            AND date BETWEEN ? AND ?
            """,
            (
                user_id,
                start_date,
                end_date,
            ),
        )

    # Calculate all spending
    else:

        cursor.execute(
            """
            SELECT COALESCE(
                SUM(amount),
                0
            )

            FROM expenses

            WHERE user_id = ?
            """,
            (user_id,),
        )

    total = cursor.fetchone()[0]

    conn.close()

    return float(total)


# =========================
# SAVE BUDGET
# =========================


def save_budget(budget):
    """Save or update the logged-in user's budget."""

    user_id = get_current_user_id()

    conn = connect_db()
    cursor = conn.cursor()

    # Check whether this user already has a budget
    cursor.execute(
        """
        SELECT id
        FROM budget
        WHERE user_id = ?
        """,
        (user_id,),
    )

    existing_budget = cursor.fetchone()

    # Update current budget
    if existing_budget:

        budget_id = existing_budget[0]

        cursor.execute(
            """
            UPDATE budget

            SET
                amount = ?,
                period = ?,
                start_date = ?,
                end_date = ?

            WHERE id = ?
            AND user_id = ?
            """,
            (
                budget.amount,
                budget.period,
                budget.start_date,
                budget.end_date,
                budget_id,
                user_id,
            ),
        )

    # Create this user's first budget
    else:

        cursor.execute(
            """
            INSERT INTO budget (
                user_id,
                amount,
                period,
                start_date,
                end_date
            )

            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                budget.amount,
                budget.period,
                budget.start_date,
                budget.end_date,
            ),
        )

        budget_id = cursor.lastrowid

    conn.commit()
    conn.close()

    budget.budget_id = budget_id

    return budget


# =========================
# GET BUDGET
# =========================


def get_budget():
    """Get the logged-in user's budget."""

    user_id = get_current_user_id()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            amount,
            period,
            start_date,
            end_date

        FROM budget

        WHERE user_id = ?
        """,
        (user_id,),
    )

    budget = cursor.fetchone()

    conn.close()

    return budget
