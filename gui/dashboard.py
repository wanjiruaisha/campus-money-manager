import tkinter as tk
from tkinter import ttk

from database import (
    get_budget,
    get_total_spent,
    get_recent_expenses
)

from utils import (
    calculate_remaining_budget,
    calculate_days_remaining,
    calculate_daily_allowance
)


class DashboardFrame(ttk.Frame):
    """Dashboard screen for Campus Money Manager."""

    def __init__(self, parent):
        super().__init__(parent)

        # Variables displayed on screen
        self.budget_var = tk.StringVar(
            value="KSh 0.00"
        )

        self.spent_var = tk.StringVar(
            value="KSh 0.00"
        )

        self.remaining_var = tk.StringVar(
            value="KSh 0.00"
        )

        self.daily_var = tk.StringVar(
            value="KSh 0.00"
        )

        self.period_var = tk.StringVar(
            value="No budget set"
        )

        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        """Create dashboard widgets."""

        title = ttk.Label(
            self,
            text="Campus Money Manager",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=(25, 5))

        subtitle = ttk.Label(
            self,
            text="Track your spending and manage your student budget."
        )

        subtitle.pack(pady=(0, 20))

        # Budget period
        period_label = ttk.Label(
            self,
            textvariable=self.period_var,
            font=("Arial", 11)
        )

        period_label.pack(pady=5)

        # Summary cards
        summary_frame = ttk.Frame(self)
        summary_frame.pack(
            fill="x",
            padx=30,
            pady=20
        )

        self.create_summary_card(
            summary_frame,
            "Budget",
            self.budget_var,
            0
        )

        self.create_summary_card(
            summary_frame,
            "Total Spent",
            self.spent_var,
            1
        )

        self.create_summary_card(
            summary_frame,
            "Remaining",
            self.remaining_var,
            2
        )

        self.create_summary_card(
            summary_frame,
            "Daily Allowance",
            self.daily_var,
            3
        )

        # Recent expenses section
        recent_frame = ttk.LabelFrame(
            self,
            text="Recent Expenses",
            padding=10
        )

        recent_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        columns = (
            "amount",
            "category",
            "description",
            "date"
        )

        self.recent_tree = ttk.Treeview(
            recent_frame,
            columns=columns,
            show="headings",
            height=7
        )

        self.recent_tree.heading(
            "amount",
            text="Amount"
        )

        self.recent_tree.heading(
            "category",
            text="Category"
        )

        self.recent_tree.heading(
            "description",
            text="Description"
        )

        self.recent_tree.heading(
            "date",
            text="Date"
        )

        self.recent_tree.column(
            "amount",
            width=100
        )

        self.recent_tree.column(
            "category",
            width=150
        )

        self.recent_tree.column(
            "description",
            width=250
        )

        self.recent_tree.column(
            "date",
            width=120
        )

        self.recent_tree.pack(
            fill="both",
            expand=True
        )

    def create_summary_card(
        self,
        parent,
        heading,
        variable,
        column
    ):
        """Create one dashboard summary card."""

        card = ttk.LabelFrame(
            parent,
            text=heading,
            padding=15
        )

        card.grid(
            row=0,
            column=column,
            padx=8,
            sticky="nsew"
        )

        parent.columnconfigure(
            column,
            weight=1
        )

        value_label = ttk.Label(
            card,
            textvariable=variable,
            font=("Arial", 15, "bold")
        )

        value_label.pack()

    def refresh(self):
        """Refresh dashboard values."""

        budget = get_budget()

        # No budget has been created yet
        if budget is None:
            self.budget_var.set("KSh 0.00")
            self.spent_var.set("KSh 0.00")
            self.remaining_var.set("KSh 0.00")
            self.daily_var.set("KSh 0.00")
            self.period_var.set(
                "No budget has been set."
            )

        else:
            (
                budget_id,
                amount,
                period,
                start_date,
                end_date
            ) = budget

            total_spent = get_total_spent(
                start_date,
                end_date
            )

            remaining = calculate_remaining_budget(
                amount,
                total_spent
            )

            days_left = calculate_days_remaining(
                end_date
            )

            daily_allowance = calculate_daily_allowance(
                remaining,
                days_left
            )

            self.budget_var.set(
                f"KSh {amount:,.2f}"
            )

            self.spent_var.set(
                f"KSh {total_spent:,.2f}"
            )

            self.remaining_var.set(
                f"KSh {remaining:,.2f}"
            )

            self.daily_var.set(
                f"KSh {daily_allowance:,.2f}"
            )

            self.period_var.set(
                f"{period} Budget: "
                f"{start_date} to {end_date}"
            )

        self.load_recent_expenses()

    def load_recent_expenses(self):
        """Display the five most recent expenses."""

        for row in self.recent_tree.get_children():
            self.recent_tree.delete(row)

        expenses = get_recent_expenses(5)

        for expense in expenses:
            expense_id, amount, category, description, expense_date = expense

            self.recent_tree.insert(
                "",
                tk.END,
                values=(
                    f"KSh {amount:,.2f}",
                    category,
                    description,
                    expense_date
                )
            )