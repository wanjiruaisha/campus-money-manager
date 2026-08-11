from tkinter import ttk

from .dashboard import DashboardFrame
from .expenses import ExpenseFrame
from .budget import BudgetFrame
from .affordability import AffordabilityFrame


class CampusMoneyApp:
    """Main graphical interface for Campus Money Manager."""

    def __init__(self, root):
        self.root = root

        # Main window settings
        self.root.title("Campus Money Manager")
        self.root.geometry("1000x650")
        self.root.minsize(850, 550)

        # Create tab navigation
        self.notebook = ttk.Notebook(self.root)

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Create screens
        self.dashboard_frame = DashboardFrame(
            self.notebook
        )

        self.expense_frame = ExpenseFrame(
            self.notebook,
            on_change=self.refresh_data
        )

        self.budget_frame = BudgetFrame(
            self.notebook,
            on_change=self.refresh_data
        )

        self.affordability_frame = AffordabilityFrame(
            self.notebook
        )

        # Add screens to navigation
        self.notebook.add(
            self.dashboard_frame,
            text="Dashboard"
        )

        self.notebook.add(
            self.expense_frame,
            text="Expenses"
        )

        self.notebook.add(
            self.budget_frame,
            text="Budget"
        )

        self.notebook.add(
            self.affordability_frame,
            text="Can I Afford This?"
        )

        # Refresh information whenever the user changes tabs
        self.notebook.bind(
            "<<NotebookTabChanged>>",
            self.on_tab_changed
        )

    def refresh_data(self):
        """Refresh application data after something changes."""

        self.dashboard_frame.refresh()
        self.expense_frame.load_expenses()

    def on_tab_changed(self, event):
        """Refresh the selected screen when changing tabs."""

        selected_tab = self.notebook.index(
            self.notebook.select()
        )

        # Dashboard
        if selected_tab == 0:
            self.dashboard_frame.refresh()

        # Expenses
        elif selected_tab == 1:
            self.expense_frame.load_expenses()

        # Budget
        elif selected_tab == 2:
            self.budget_frame.load_budget()