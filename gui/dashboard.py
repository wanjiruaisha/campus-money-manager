import tkinter as tk
from tkinter import ttk


class DashboardFrame(ttk.Frame):
    """Dashboard screen for the Campus Money Manager."""

    def __init__(self, parent):
        super().__init__(parent)

        self.create_widgets()

    def create_widgets(self):
        """Create the dashboard interface."""

        title = ttk.Label(
            self,
            text="Campus Money Manager",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=40)

        description = ttk.Label(
            self,
            text=(
                "Manage your budget, record your daily expenses,\n"
                "and keep track of your campus spending."
            ),
            font=("Arial", 12),
            justify="center"
        )
        description.pack(pady=10)