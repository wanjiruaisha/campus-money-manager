import tkinter as tk
from tkinter import ttk, messagebox

import customtkinter as ctk

from database import (
    get_budget,
    get_total_spent,
)

from utils import (
    calculate_remaining_budget,
    calculate_days_remaining,
    calculate_daily_allowance,
)


class AffordabilityFrame(ttk.Frame):
    """Screen used to show how a planned purchase affects the budget."""

    def __init__(self, parent):
        super().__init__(parent)

        # Scrollable area inside the Notebook tab
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#F4F7FB",
            corner_radius=0,
        )

        self.scrollable_frame.pack(
            fill="both",
            expand=True,
        )

        # Values displayed before purchase
        self.current_remaining_var = tk.StringVar(
            value="KSh 0.00"
        )

        self.current_daily_var = tk.StringVar(
            value="KSh 0.00"
        )

        # Values displayed after purchase
        self.after_remaining_var = tk.StringVar(
            value="KSh 0.00"
        )

        self.after_daily_var = tk.StringVar(
            value="KSh 0.00"
        )

        # Recommendation/result
        self.result_var = tk.StringVar(
            value="Enter a purchase amount to see its impact."
        )

        self.create_widgets()

    def create_widgets(self):
        """Create the purchase planner interface."""

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
            text="Purchase Planner",
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
            text=(
                "See how a planned purchase would affect "
                "your remaining budget and daily allowance."
            ),
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
        # PURCHASE INPUT
        # =========================

        purchase_card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="white",
            corner_radius=16,
        )

        purchase_card.pack(
            fill="x",
            padx=25,
            pady=10,
        )

        purchase_title = ctk.CTkLabel(
            purchase_card,
            text="Planned Purchase",
            text_color="#1F2937",
            font=ctk.CTkFont(
                size=16,
                weight="bold",
            ),
        )

        purchase_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 10),
        )

        self.purchase_entry = ctk.CTkEntry(
            purchase_card,
            placeholder_text="Enter purchase amount e.g. 1800",
            height=42,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.purchase_entry.pack(
            fill="x",
            padx=25,
            pady=(0, 15),
        )

        check_button = ctk.CTkButton(
            purchase_card,
            text="Check Purchase Impact",
            command=self.check_purchase,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            corner_radius=10,
            height=40,
        )

        check_button.pack(
            pady=(0, 20),
        )

        # =========================
        # BEFORE / AFTER SECTION
        # =========================

        comparison_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="transparent",
        )

        comparison_frame.pack(
            fill="x",
            padx=20,
            pady=10,
        )

        comparison_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        comparison_frame.grid_columnconfigure(
            1,
            weight=1,
        )

        # -------------------------
        # BEFORE PURCHASE
        # -------------------------

        before_card = ctk.CTkFrame(
            comparison_frame,
            fg_color="#DBEAFE",
            corner_radius=16,
        )

        before_card.grid(
            row=0,
            column=0,
            padx=5,
            sticky="nsew",
        )

        before_title = ctk.CTkLabel(
            before_card,
            text="Before Purchase",
            text_color="#1D4ED8",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
        )

        before_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 12),
        )

        ctk.CTkLabel(
            before_card,
            text="Remaining Budget",
            text_color="#4B5563",
            font=ctk.CTkFont(
                size=11,
            ),
        ).pack(
            anchor="w",
            padx=20,
        )

        ctk.CTkLabel(
            before_card,
            textvariable=self.current_remaining_var,
            text_color="#1D4ED8",
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        ).pack(
            anchor="w",
            padx=20,
            pady=(2, 12),
        )

        ctk.CTkLabel(
            before_card,
            text="Daily Allowance",
            text_color="#4B5563",
            font=ctk.CTkFont(
                size=11,
            ),
        ).pack(
            anchor="w",
            padx=20,
        )

        ctk.CTkLabel(
            before_card,
            textvariable=self.current_daily_var,
            text_color="#1D4ED8",
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        ).pack(
            anchor="w",
            padx=20,
            pady=(2, 18),
        )

        # -------------------------
        # AFTER PURCHASE
        # -------------------------

        after_card = ctk.CTkFrame(
            comparison_frame,
            fg_color="#F8FAFC",
            corner_radius=16,
            border_width=1,
            border_color="#E2E8F0",
        )

        after_card.grid(
            row=0,
            column=1,
            padx=5,
            sticky="nsew",
        )

        after_title = ctk.CTkLabel(
            after_card,
            text="After Purchase",
            text_color="#1F2937",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
        )

        after_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 12),
        )

        ctk.CTkLabel(
            after_card,
            text="Remaining Budget",
            text_color="#4B5563",
            font=ctk.CTkFont(
                size=11,
            ),
        ).pack(
            anchor="w",
            padx=20,
        )

        self.after_remaining_label = ctk.CTkLabel(
            after_card,
            textvariable=self.after_remaining_var,
            text_color="#1F2937",
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        )

        self.after_remaining_label.pack(
            anchor="w",
            padx=20,
            pady=(2, 12),
        )

        ctk.CTkLabel(
            after_card,
            text="New Daily Allowance",
            text_color="#4B5563",
            font=ctk.CTkFont(
                size=11,
            ),
        ).pack(
            anchor="w",
            padx=20,
        )

        self.after_daily_label = ctk.CTkLabel(
            after_card,
            textvariable=self.after_daily_var,
            text_color="#1F2937",
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        )

        self.after_daily_label.pack(
            anchor="w",
            padx=20,
            pady=(2, 18),
        )

        # =========================
        # RESULT / GUIDANCE
        # =========================

        self.result_card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#F8FAFC",
            corner_radius=16,
            border_width=1,
            border_color="#E2E8F0",
        )

        self.result_card.pack(
            fill="x",
            padx=25,
            pady=(10, 25),
        )

        result_title = ctk.CTkLabel(
            self.result_card,
            text="Purchase Impact",
            text_color="#1F2937",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
        )

        result_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 8),
        )

        self.result_label = ctk.CTkLabel(
            self.result_card,
            textvariable=self.result_var,
            text_color="#475569",
            wraplength=750,
            justify="left",
            font=ctk.CTkFont(
                size=12,
            ),
        )

        self.result_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 18),
        )

    def check_purchase(self):
        """Calculate how a planned purchase affects the budget."""

        purchase = self.purchase_entry.get().strip()

        # Validate purchase amount
        try:
            purchase = float(purchase)

            if purchase <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Enter a valid purchase amount greater than zero.",
            )
            return

        # Get current budget
        budget = get_budget()

        if budget is None:
            messagebox.showwarning(
                "No Budget",
                "Please set a budget first.",
            )
            return

        (
            budget_id,
            budget_amount,
            period,
            start_date,
            end_date,
        ) = budget

        # Get total spending during the current budget period
        total_spent = get_total_spent(
            start_date,
            end_date,
        )

        # Calculate current remaining money
        remaining = calculate_remaining_budget(
            budget_amount,
            total_spent,
        )

        # Calculate days remaining
        days_left = calculate_days_remaining(
            end_date
        )

        # Current daily allowance
        current_daily = calculate_daily_allowance(
            remaining,
            days_left,
        )

        # Calculate money remaining after purchase
        remaining_after = (
            remaining - purchase
        )

        # Calculate daily allowance after purchase
        if remaining_after > 0:
            daily_after = calculate_daily_allowance(
                remaining_after,
                days_left,
            )

        else:
            daily_after = 0

        # -------------------------
        # DISPLAY BEFORE VALUES
        # -------------------------

        self.current_remaining_var.set(
            f"KSh {remaining:,.2f}"
        )

        self.current_daily_var.set(
            f"KSh {current_daily:,.2f} / day"
        )

        # -------------------------
        # DISPLAY AFTER VALUES
        # -------------------------

        self.after_remaining_var.set(
            f"KSh {remaining_after:,.2f}"
        )

        self.after_daily_var.set(
            f"KSh {daily_after:,.2f} / day"
        )

        # -------------------------
        # RESULT
        # -------------------------

        if remaining_after < 0:

            exceeded_by = abs(
                remaining_after
            )

            self.result_var.set(
                (
                    f"This purchase would exceed your remaining "
                    f"budget by KSh {exceeded_by:,.2f}."
                )
            )

            self.result_card.configure(
                fg_color="#FEE2E2",
                border_color="#FCA5A5",
            )

            self.result_label.configure(
                text_color="#DC2626"
            )

            self.after_remaining_label.configure(
                text_color="#DC2626"
            )

            self.after_daily_label.configure(
                text_color="#DC2626"
            )

        else:

            self.result_var.set(
                (
                    f"This purchase fits within your remaining budget. "
                    f"Your daily allowance would change from "
                    f"KSh {current_daily:,.2f} to "
                    f"KSh {daily_after:,.2f} for the remaining "
                    f"{days_left} day(s)."
                )
            )

            self.result_card.configure(
                fg_color="#DCFCE7",
                border_color="#86EFAC",
            )

            self.result_label.configure(
                text_color="#15803D"
            )

            self.after_remaining_label.configure(
                text_color="#15803D"
            )

            self.after_daily_label.configure(
                text_color="#15803D"
            )