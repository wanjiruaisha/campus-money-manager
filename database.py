import sqlite3


# Name of the SQLite database file
DATABASE_NAME = "campus_money.db"


def connect_db():
    """Create and return a connection to the database."""

    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    """Create the application's database tables."""

    conn = connect_db()
    cursor = conn.cursor()

    # Create table for expenses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    # Create table for budget information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            period TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT
        )
    """)

    # Save the changes
    conn.commit()

    # Close the connection
    conn.close()