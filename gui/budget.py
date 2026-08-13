import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

import customtkinter as ctk

from models import Budget

from database import (
    save_budget,
    get_budget,
)


class BudgetFrame(ttk.Frame):
    """Screen used to create and update a budget."""

    def __init__(self, parent, on_change=None):
        super().__init__(parent)

        self.on_change = on_change

        # Scrollable CustomTkinter area inside the Notebook tab
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#F4F7FB",
            corner_radius=0,
        )

        self.scrollable_frame.pack(
            fill="both",
            expand=True,
        )

        self.create_widgets()
        self.load_budget()

    def create_widgets(self):
        """Create the budget management interface."""

        # =========================
        # PAGE HEADING
        # =========================

        heading_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#2563EB",
            corner_radius=18,
        )

        heading_frame.pack(
            fill="x",
            padx=25,
            pady=(20, 15),
        )

        title = ctk.CTkLabel(
            heading_frame,
            text="Budget Management",
            text_color="white",
            font=ctk.CTkFont(
                size=22,
                weight="bold",
            ),
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(20, 4),
        )

        subtitle = ctk.CTkLabel(
            heading_frame,
            text=("Set how much money you want to use " "for the week or month."),
            text_color="#DBEAFE",
            font=ctk.CTkFont(
                size=12,
            ),
        )

        subtitle.pack(
            anchor="w",
            padx=25,
            pady=(0, 20),
        )

        # =========================
        # BUDGET FORM CARD
        # =========================

        form_card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="white",
            corner_radius=16,
        )

        form_card.pack(
            fill="x",
            padx=25,
            pady=10,
        )

        form_title = ctk.CTkLabel(
            form_card,
            text="Budget Details",
            text_color="#1F2937",
            font=ctk.CTkFont(
                size=16,
                weight="bold",
            ),
        )

        form_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 15),
        )

        form = ctk.CTkFrame(
            form_card,
            fg_color="transparent",
        )

        form.pack(
            fill="x",
            padx=25,
            pady=(0, 25),
        )

        form.grid_columnconfigure(
            1,
            weight=1,
        )

        # =========================
        # BUDGET AMOUNT
        # =========================

        amount_label = ctk.CTkLabel(
            form,
            text="Budget Amount",
            text_color="#374151",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        amount_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=10,
        )

        self.amount_entry = ctk.CTkEntry(
            form,
            placeholder_text="e.g. 5000",
            height=40,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.amount_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            pady=10,
        )

        # =========================
        # BUDGET PERIOD
        # =========================

        period_label = ctk.CTkLabel(
            form,
            text="Budget Period",
            text_color="#374151",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        period_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=10,
        )

        self.period_combo = ctk.CTkComboBox(
            form,
            values=[
                "Weekly",
                "Monthly",
            ],
            state="readonly",
            height=40,
            corner_radius=10,
            border_color="#CBD5E1",
            button_color="#2563EB",
            button_hover_color="#1D4ED8",
            dropdown_hover_color="#DBEAFE",
        )

        self.period_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=10,
        )

        self.period_combo.set("Weekly")

        # =========================
        # START DATE
        # =========================

        start_label = ctk.CTkLabel(
            form,
            text="Start Date",
            text_color="#374151",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        start_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=10,
        )

        self.start_date_entry = ctk.CTkEntry(
            form,
            placeholder_text="YYYY-MM-DD",
            height=40,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.start_date_entry.grid(
            row=2,
            column=1,
            sticky="ew",
            pady=10,
        )

        # =========================
        # END DATE
        # =========================

        end_label = ctk.CTkLabel(
            form,
            text="End Date",
            text_color="#374151",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        end_label.grid(
            row=3,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=10,
        )

        self.end_date_entry = ctk.CTkEntry(
            form,
            placeholder_text="YYYY-MM-DD",
            height=40,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.end_date_entry.grid(
            row=3,
            column=1,
            sticky="ew",
            pady=10,
        )

        date_hint = ctk.CTkLabel(
            form,
            text="Use YYYY-MM-DD format",
            text_color="#6B7280",
            font=ctk.CTkFont(
                size=10,
            ),
        )

        date_hint.grid(
            row=4,
            column=1,
            sticky="w",
            pady=(0, 10),
        )

        # =========================
        # SAVE BUTTON
        # =========================

        save_button = ctk.CTkButton(
            form,
            text="Save Budget",
            command=self.save,
            fg_color="#16A34A",
            hover_color="#15803D",
            corner_radius=10,
            height=40,
        )

        save_button.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=(15, 5),
        )

        # =========================
        # INFORMATION CARD
        # =========================

        info_card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#DBEAFE",
            corner_radius=16,
        )

        info_card.pack(
            fill="x",
            padx=25,
            pady=(10, 25),
        )

        info_title = ctk.CTkLabel(
            info_card,
            text="💡 How your budget works",
            text_color="#1D4ED8",
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
        )

        info_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 5),
        )

        info_text = ctk.CTkLabel(
            info_card,
            text=(
                "Your expenses are compared with this budget. "
                "Campus Money Manager then calculates how much "
                "you have spent, how much remains, and your "
                "recommended daily allowance."
            ),
            text_color="#374151",
            wraplength=700,
            justify="left",
            font=ctk.CTkFont(
                size=11,
            ),
        )

        info_text.pack(
            anchor="w",
            padx=20,
            pady=(0, 18),
        )

    # =========================
    # SAVE BUDGET
    # =========================

    def save(self):
        """Validate and save the budget."""

        amount = self.amount_entry.get().strip()
        period = self.period_combo.get().strip()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()

        # Check that all fields are filled
        if not amount or not period or not start_date or not end_date:
            messagebox.showerror(
                "Missing Information",
                "Please complete all budget fields.",
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
                "Budget amount must be greater than zero.",
            )
            return

        # Validate dates
        try:
            start = datetime.strptime(
                start_date,
                "%Y-%m-%d",
            )

            end = datetime.strptime(
                end_date,
                "%Y-%m-%d",
            )

        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Please use YYYY-MM-DD format.",
            )
            return

        # End date cannot be before start date
        if end < start:
            messagebox.showerror(
                "Invalid Date Range",
                "End date cannot be before start date.",
            )
            return

        # Create Budget object
        budget = Budget(
            amount=amount,
            period=period,
            start_date=start_date,
            end_date=end_date,
        )

        # Save it to SQLite
        save_budget(budget)

        messagebox.showinfo(
            "Success",
            "Budget saved successfully.",
        )

        # Refresh dashboard
        if self.on_change:
            self.on_change()

    # =========================
    # LOAD BUDGET
    # =========================

    def load_budget(self):
        """Load the current budget into the form."""

        budget = get_budget()

        # Clear current form
        self.amount_entry.delete(
            0,
            tk.END,
        )

        self.period_combo.set("Weekly")

        self.start_date_entry.delete(
            0,
            tk.END,
        )

        self.end_date_entry.delete(
            0,
            tk.END,
        )

        # If there is no saved budget yet
        if budget is None:

            # Start with today's date
            self.start_date_entry.insert(
                0,
                date.today().isoformat(),
            )

            return

        # Existing budget
        (
            budget_id,
            amount,
            period,
            start_date,
            end_date,
        ) = budget

        # Put saved values into form
        self.amount_entry.insert(
            0,
            amount,
        )

        self.period_combo.set(period)

        self.start_date_entry.insert(
            0,
            start_date,
        )

        self.end_date_entry.insert(
            0,
            end_date,
        )
