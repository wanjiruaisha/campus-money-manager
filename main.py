import customtkinter as ctk

from database import create_tables
from gui import CampusMoneyApp


def main():
    """Start the Campus Money Manager application."""

     # Set CustomTkinter appearance
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # Create database tables
    create_tables()

    # Create the main CustomTkinter window
    root = ctk.CTk()

    # Start application interface
    CampusMoneyApp(root)

    # Keep application running
    root.mainloop()


if __name__ == "__main__":
    main()