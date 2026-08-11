import tkinter as tk


def main():
    """Start the Campus Money Manager application."""

    # Create the main window
    root = tk.Tk()

    # Set the title displayed at the top of the window
    root.title("Campus Money Manager")

    # Set the starting window size
    root.geometry("900x600")

    # Prevent the window from becoming too small
    root.minsize(700, 500)

    # Keep the application running
    root.mainloop()


if __name__ == "__main__":
    main()