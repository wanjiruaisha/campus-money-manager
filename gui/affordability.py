import tkinter as tk

from tkinter import (
    ttk,
    messagebox
)

from database import (
    get_budget,
    get_total_spent
)

from utils import (
    calculate_remaining_budget,
    calculate_days_remaining,
    check_affordability
)


class AffordabilityFrame(ttk.Frame):
    """Screen used to check whether a purchase fits the budget."""

    def __init__(self, parent):
        super().__init__(parent)

        self.status_var = tk.StringVar(
            value="Enter a purchase amount to check."
        )

        self.remaining_var = tk.StringVar(
            value="-"
        )

        self.after_var = tk.StringVar(
            value="-"
        )

        self.daily_var = tk.StringVar(
            value="-"
        )

        self.create_widgets()

    def create_widgets(self):
        """Create affordability interface."""

        title = ttk.Label(
            self,
            text="Can I Afford This?",
            font=("Arial", 22, "bold")
        )

        title.pack(
            pady=(40, 10)
        )

        description = ttk.Label(
            self,
            text=(
                "Enter the cost of a planned purchase to see "
                "whether it fits within your current budget."
            ),
            wraplength=600,
            justify="center"
        )

        description.pack(
            pady=10
        )

        form = ttk.LabelFrame(
            self,
            text="Purchase",
            padding=20
        )

        form.pack(
            padx=40,
            pady=20,
            fill="x"
        )

        ttk.Label(
            form,
            text="Purchase Amount:"
        ).pack(
            pady=5
        )

        self.purchase_entry = ttk.Entry(
            form,
            width=30
        )

        self.purchase_entry.pack(
            pady=10
        )

        check_button = ttk.Button(
            form,
            text="Check Affordability",
            command=self.check_purchase
        )

        check_button.pack(
            pady=10
        )

        # Results
        result_frame = ttk.LabelFrame(
            self,
            text="Result",
            padding=20
        )

        result_frame.pack(
            padx=40,
            pady=20,
            fill="x"
        )

        ttk.Label(
            result_frame,
            textvariable=self.status_var,
            font=("Arial", 14, "bold")
        ).pack(
            pady=10
        )

        ttk.Label(
            result_frame,
            textvariable=self.remaining_var
        ).pack(
            pady=5
        )

        ttk.Label(
            result_frame,
            textvariable=self.after_var
        ).pack(
            pady=5
        )

        ttk.Label(
            result_frame,
            textvariable=self.daily_var
        ).pack(
            pady=5
        )

    def check_purchase(self):
        """Check whether a planned purchase fits the budget."""

        purchase = self.purchase_entry.get().strip()

        try:
            purchase = float(
                purchase
            )

            if purchase <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Enter a valid purchase amount greater than zero."
            )
            return

        budget = get_budget()

        if budget is None:
            messagebox.showwarning(
                "No Budget",
                "Please set a budget first."
            )
            return

        (
            budget_id,
            budget_amount,
            period,
            start_date,
            end_date
        ) = budget

        total_spent = get_total_spent(
            start_date,
            end_date
        )

        remaining = calculate_remaining_budget(
            budget_amount,
            total_spent
        )

        days_left = calculate_days_remaining(
            end_date
        )

        (
            affordable,
            remaining_after,
            daily_after
        ) = check_affordability(
            remaining,
            purchase,
            days_left
        )

        self.remaining_var.set(
            f"Current remaining budget: "
            f"KSh {remaining:,.2f}"
        )

        self.after_var.set(
            f"Money after purchase: "
            f"KSh {remaining_after:,.2f}"
        )

        self.daily_var.set(
            f"Daily allowance after purchase: "
            f"KSh {daily_after:,.2f}"
        )

        if affordable:
            self.status_var.set(
                "✓ This purchase fits within your current budget."
            )

        else:
            self.status_var.set(
                "✗ This purchase exceeds your remaining budget."
            )