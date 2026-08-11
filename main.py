import tkinter as tk

from database import create_tables
from gui import CampusMoneyApp


def main():
    """Start the Campus Money Manager application."""

    # Create database tables
    create_tables()

    # Create main window
    root = tk.Tk()

    # Start application interface
    CampusMoneyApp(root)

    # Keep application running
    root.mainloop()


if __name__ == "__main__":
    main()