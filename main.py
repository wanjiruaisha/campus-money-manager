import tkinter as tk

from database import create_tables


def main():
    """Start the Campus Money Manager application."""

    # Create database tables when the application starts
    create_tables()

    # Create the main window
    root = tk.Tk()

    root.title("Campus Money Manager")
    root.geometry("900x600")
    root.minsize(700, 500)

    root.mainloop()


if __name__ == "__main__":
    main()