import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

from database import (
    get_budget,
    get_total_spent,
    get_recent_expenses,
)

from utils import (
    calculate_remaining_budget,
    calculate_days_remaining,
    calculate_daily_allowance,
)


class DashboardFrame(ttk.Frame):
    """Main dashboard and welcome screen."""

    def __init__(self, parent):
        super().__init__(parent)

        # The parent is the ttk Notebook
        self.notebook = parent

        # Create a CustomTkinter scrollable area
        # INSIDE the normal ttk.Frame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#F4F7FB",
            corner_radius=0,
        )

        self.scrollable_frame.pack(
            fill="both",
            expand=True,
        )

        # Dashboard values
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

        self.progress_text_var = tk.StringVar(
            value="0% of budget spent"
        )

        self.days_left_var = tk.StringVar(
            value=""
        )

        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        """Create the dashboard interface."""

        # =========================
        # WELCOME SECTION
        # =========================

        hero_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#2563EB",
            corner_radius=20,
        )

        hero_frame.pack(
            fill="x",
            padx=25,
            pady=(20, 15),
        )

        hero_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        # Welcome title
        title = ctk.CTkLabel(
            hero_frame,
            text="Welcome to Campus Money Manager",
            text_color="white",
            font=ctk.CTkFont(
                size=24,
                weight="bold",
            ),
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=25,
            pady=(22, 5),
        )

        # Description
        subtitle = ctk.CTkLabel(
            hero_frame,
            text=(
                "Track your spending, manage your budget, "
                "and make your money last."
            ),
            text_color="#DBEAFE",
            font=ctk.CTkFont(
                size=13
            ),
        )

        subtitle.grid(
            row=1,
            column=0,
            sticky="w",
            padx=25,
            pady=(0, 5),
        )

        # Small visual
        money_icon = ctk.CTkLabel(
            hero_frame,
            text="💰 📊",
            text_color="white",
            font=ctk.CTkFont(
                size=30
            ),
        )

        money_icon.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=25,
        )

        # Current budget period
        period_label = ctk.CTkLabel(
            hero_frame,
            textvariable=self.period_var,
            text_color="white",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        period_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=25,
            pady=(5, 2),
        )

        # Days remaining
        days_label = ctk.CTkLabel(
            hero_frame,
            textvariable=self.days_left_var,
            text_color="#DBEAFE",
            font=ctk.CTkFont(
                size=11
            ),
        )

        days_label.grid(
            row=3,
            column=0,
            sticky="w",
            padx=25,
            pady=(0, 22),
        )

        # =========================
        # SUMMARY CARDS
        # =========================

        cards_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="transparent",
        )

        cards_frame.pack(
            fill="x",
            padx=20,
            pady=5,
        )

        # Two columns make it work better
        # on smaller screens
        cards_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        cards_frame.grid_columnconfigure(
            1,
            weight=1,
        )

        # Budget card
        self.create_summary_card(
            parent=cards_frame,
            title="Budget",
            value=self.budget_var,
            icon="💵",
            background="#DBEAFE",
            text_color="#1D4ED8",
            row=0,
            column=0,
        )

        # Total spent card
        self.create_summary_card(
            parent=cards_frame,
            title="Total Spent",
            value=self.spent_var,
            icon="🧾",
            background="#FEE2E2",
            text_color="#DC2626",
            row=0,
            column=1,
        )

        # Remaining card
        self.create_summary_card(
            parent=cards_frame,
            title="Remaining",
            value=self.remaining_var,
            icon="💼",
            background="#DCFCE7",
            text_color="#15803D",
            row=1,
            column=0,
        )

        # Daily allowance card
        self.create_summary_card(
            parent=cards_frame,
            title="Daily Allowance",
            value=self.daily_var,
            icon="📅",
            background="#FEF3C7",
            text_color="#B45309",
            row=1,
            column=1,
        )

        # =========================
        # BUDGET PROGRESS
        # =========================

        progress_card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="white",
            corner_radius=16,
        )

        progress_card.pack(
            fill="x",
            padx=25,
            pady=15,
        )

        progress_title = ctk.CTkLabel(
            progress_card,
            text="Budget Progress",
            text_color="#1F2937",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
        )

        progress_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 8),
        )

        self.progress_bar = ctk.CTkProgressBar(
            progress_card,
            height=14,
            corner_radius=8,
            progress_color="#2563EB",
            fg_color="#E5E7EB",
        )

        self.progress_bar.pack(
            fill="x",
            padx=20,
            pady=5,
        )

        # Start at 0%
        self.progress_bar.set(0)

        progress_text = ctk.CTkLabel(
            progress_card,
            textvariable=self.progress_text_var,
            text_color="#6B7280",
            font=ctk.CTkFont(
                size=11
            ),
        )

        progress_text.pack(
            anchor="w",
            padx=20,
            pady=(5, 18),
        )

        # =========================
        # QUICK ACTIONS
        # =========================

        quick_card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="white",
            corner_radius=16,
        )

        quick_card.pack(
            fill="x",
            padx=25,
            pady=10,
        )

        quick_title = ctk.CTkLabel(
            quick_card,
            text="Quick Actions",
            text_color="#1F2937",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
        )

        quick_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 10),
        )

        button_frame = ctk.CTkFrame(
            quick_card,
            fg_color="transparent",
        )

        button_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 18),
        )

        button_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        button_frame.grid_columnconfigure(
            1,
            weight=1,
        )

        button_frame.grid_columnconfigure(
            2,
            weight=1,
        )

        # Add expense
        add_button = ctk.CTkButton(
            button_frame,
            text="+ Add Expense",
            fg_color="#16A34A",
            hover_color="#15803D",
            corner_radius=10,
            command=lambda: self.notebook.select(1),
        )

        add_button.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="ew",
        )

        # Set budget
        budget_button = ctk.CTkButton(
            button_frame,
            text="Set Budget",
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            corner_radius=10,
            command=lambda: self.notebook.select(2),
        )

        budget_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky="ew",
        )

        # Affordability
        afford_button = ctk.CTkButton(
            button_frame,
            text="Purchase Planner",
            fg_color="#7C3AED",
            hover_color="#6D28D9",
            corner_radius=10,
            command=lambda: self.notebook.select(3),
        )

        afford_button.grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky="ew",
        )

        # =========================
        # RECENT EXPENSES
        # =========================

        recent_card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="white",
            corner_radius=16,
        )

        recent_card.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(10, 25),
        )

        recent_title = ctk.CTkLabel(
            recent_card,
            text="Recent Expenses",
            text_color="#1F2937",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
        )

        recent_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 10),
        )

        # CustomTkinter does not have a table widget,
        # so we continue using ttk.Treeview.
        columns = (
            "amount",
            "category",
            "description",
            "date",
        )

        self.recent_tree = ttk.Treeview(
            recent_card,
            columns=columns,
            show="headings",
            height=6,
        )

        self.recent_tree.heading(
            "amount",
            text="Amount",
        )

        self.recent_tree.heading(
            "category",
            text="Category",
        )

        self.recent_tree.heading(
            "description",
            text="Description",
        )

        self.recent_tree.heading(
            "date",
            text="Date",
        )

        self.recent_tree.column(
            "amount",
            width=120,
        )

        self.recent_tree.column(
            "category",
            width=150,
        )

        self.recent_tree.column(
            "description",
            width=260,
        )

        self.recent_tree.column(
            "date",
            width=120,
        )

        self.recent_tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20),
        )

    def create_summary_card(
        self,
        parent,
        title,
        value,
        icon,
        background,
        text_color,
        row,
        column,
    ):
        """Create one dashboard summary card."""

        card = ctk.CTkFrame(
            parent,
            fg_color=background,
            corner_radius=16,
        )

        card.grid(
            row=row,
            column=column,
            padx=6,
            pady=6,
            sticky="nsew",
        )

        # Icon
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(
                size=22
            ),
        )

        icon_label.pack(
            anchor="w",
            padx=18,
            pady=(15, 3),
        )

        # Card title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            text_color="#4B5563",
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
        )

        title_label.pack(
            anchor="w",
            padx=18,
        )

        # Card value
        value_label = ctk.CTkLabel(
            card,
            textvariable=value,
            text_color=text_color,
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        )

        value_label.pack(
            anchor="w",
            padx=18,
            pady=(3, 15),
        )

    def refresh(self):
        """Refresh dashboard information."""

        budget = get_budget()

        # No budget has been created yet
        if budget is None:
            self.budget_var.set(
                "KSh 0.00"
            )

            self.spent_var.set(
                "KSh 0.00"
            )

            self.remaining_var.set(
                "KSh 0.00"
            )

            self.daily_var.set(
                "KSh 0.00"
            )

            self.period_var.set(
                "No budget has been set yet."
            )

            self.days_left_var.set(
                "Set a budget to begin tracking."
            )

            self.progress_bar.set(0)

            self.progress_text_var.set(
                "0% of budget spent"
            )

        else:
            (
                budget_id,
                amount,
                period,
                start_date,
                end_date,
            ) = budget

            # Get spending inside the current budget period
            total_spent = get_total_spent(
                start_date,
                end_date,
            )

            # Remaining money
            remaining = calculate_remaining_budget(
                amount,
                total_spent,
            )

            # Days remaining
            days_left = calculate_days_remaining(
                end_date
            )

            # Recommended daily allowance
            daily_allowance = calculate_daily_allowance(
                remaining,
                days_left,
            )

            # Update dashboard cards
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

            # Budget period
            self.period_var.set(
                f"{period} Budget • "
                f"{start_date} to {end_date}"
            )

            # Days remaining text
            if days_left == 1:
                self.days_left_var.set(
                    "1 day remaining in this budget."
                )

            elif days_left <= 0:
                self.days_left_var.set(
                    "This budget period has ended."
                )

            else:
                self.days_left_var.set(
                    f"{days_left} days remaining in this budget."
                )

            # Calculate percentage spent
            if amount > 0:
                percentage_spent = (
                    total_spent / amount
                ) * 100

            else:
                percentage_spent = 0

            # CTkProgressBar expects a value from 0 to 1
            progress_value = (
                percentage_spent / 100
            )

            # Keep progress bar between 0 and 1
            progress_value = max(
                0,
                min(progress_value, 1),
            )

            self.progress_bar.set(
                progress_value
            )

            self.progress_text_var.set(
                f"{percentage_spent:.0f}% of budget spent"
            )

        # Refresh recent expenses
        self.load_recent_expenses()

    def load_recent_expenses(self):
        """Display the five most recent expenses."""

        # Remove old rows
        for row in self.recent_tree.get_children():
            self.recent_tree.delete(row)

        # Get five newest expenses
        expenses = get_recent_expenses(5)

        for expense in expenses:
            (
                expense_id,
                amount,
                category,
                description,
                expense_date,
            ) = expense

            self.recent_tree.insert(
                "",
                tk.END,
                values=(
                    f"KSh {amount:,.2f}",
                    category,
                    description,
                    expense_date,
                ),
            )