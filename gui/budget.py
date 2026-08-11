import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

from models import Budget

from database import (
    save_budget,
    get_budget
)


class BudgetFrame(ttk.Frame):
    """Screen used to create and update a budget."""

    def __init__(self, parent, on_change=None):
        super().__init__(parent)

        self.on_change = on_change

        self.create_widgets()
        self.load_budget()

    def create_widgets(self):
        """Create the budget form."""

        title = ttk.Label(
            self,
            text="Budget Management",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=30)

        form = ttk.LabelFrame(
            self,
            text="Budget Details",
            padding=20
        )
        form.pack(
            padx=30,
            pady=20,
            fill="x"
        )

        form.columnconfigure(1, weight=1)

        # Budget amount
        ttk.Label(
            form,
            text="Budget Amount:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        self.amount_entry = ttk.Entry(form)

        self.amount_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=10,
            pady=10
        )

        # Budget period
        ttk.Label(
            form,
            text="Budget Period:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        self.period_combo = ttk.Combobox(
            form,
            values=("Weekly", "Monthly"),
            state="readonly"
        )

        self.period_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=10,
            pady=10
        )

        # Start date
        ttk.Label(
            form,
            text="Start Date:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        self.start_date_entry = ttk.Entry(form)

        self.start_date_entry.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=10,
            pady=10
        )

        # End date
        ttk.Label(
            form,
            text="End Date:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        self.end_date_entry = ttk.Entry(form)

        self.end_date_entry.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=10,
            pady=10
        )

        ttk.Label(
            form,
            text="Use YYYY-MM-DD format"
        ).grid(
            row=4,
            column=1,
            sticky="w",
            padx=10
        )

        save_button = ttk.Button(
            form,
            text="Save Budget",
            command=self.save
        )

        save_button.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=20
        )

    def save(self):
        """Validate and save the budget."""

        amount = self.amount_entry.get().strip()
        period = self.period_combo.get().strip()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()

        # Check that all fields have values
        if not amount or not period or not start_date or not end_date:
            messagebox.showerror(
                "Missing Information",
                "Please complete all budget fields."
            )
            return

        # Validate budget amount
        try:
            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Budget amount must be greater than zero."
            )
            return

        # Validate dates
        try:
            start = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            )

            end = datetime.strptime(
                end_date,
                "%Y-%m-%d"
            )

        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Please use YYYY-MM-DD format."
            )
            return

        # Make sure end date is after start date
        if end < start:
            messagebox.showerror(
                "Invalid Date Range",
                "End date cannot be before start date."
            )
            return

        # Create Budget object
        budget = Budget(
            amount=amount,
            period=period,
            start_date=start_date,
            end_date=end_date
        )

        # Save budget to SQLite
        save_budget(budget)

        messagebox.showinfo(
            "Success",
            "Budget saved successfully."
        )

        # Refresh other screens
        if self.on_change:
            self.on_change()

    def load_budget(self):
        """Load the current budget into the form."""

        budget = get_budget()

        # Clear current form values
        self.amount_entry.delete(0, tk.END)
        self.period_combo.set("")
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)

        # If no budget exists yet
        if budget is None:
            self.period_combo.set("Weekly")

            self.start_date_entry.insert(
                0,
                date.today().isoformat()
            )

            return

        # Get budget values from database
        budget_id, amount, period, start_date, end_date = budget

        self.amount_entry.insert(
            0,
            amount
        )

        self.period_combo.set(
            period
        )

        self.start_date_entry.insert(
            0,
            start_date
        )

        self.end_date_entry.insert(
            0,
            end_date
        )