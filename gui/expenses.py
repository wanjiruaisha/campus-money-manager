import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

import customtkinter as ctk

from models import Expense

from database import (
    add_expense,
    get_expenses,
    update_expense,
    delete_expense,
    get_budget,
    get_total_spent,
)


class ExpenseFrame(ttk.Frame):
    """Screen used to manage expenses."""

    def __init__(self, parent, on_change=None):
        super().__init__(parent)

        self.on_change = on_change

        # ID of the expense currently being edited
        self.selected_expense_id = None

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

        self.create_widgets()
        self.load_expenses()

    def create_widgets(self):
        """Create the expense management interface."""

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
            text="Expense Management",
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
            text="Record and keep track of your daily spending.",
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
        # EXPENSE FORM CARD
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
            text="Add Expense",
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
            pady=(0, 20),
        )

        form.grid_columnconfigure(
            1,
            weight=1,
        )

        # =========================
        # AMOUNT
        # =========================

        amount_label = ctk.CTkLabel(
            form,
            text="Amount",
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
            pady=8,
        )

        self.amount_entry = ctk.CTkEntry(
            form,
            placeholder_text="e.g. 250",
            height=38,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.amount_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            pady=8,
        )

        # =========================
        # CATEGORY
        # =========================

        category_label = ctk.CTkLabel(
            form,
            text="Category",
            text_color="#374151",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        category_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8,
        )

        self.category_combo = ctk.CTkComboBox(
            form,
            values=[
                "Food",
                "Transport",
                "School",
                "Printing",
                "Airtime and Data",
                "Entertainment",
                "Personal Expenses",
                "Other",
            ],
            state="readonly",
            height=38,
            corner_radius=10,
            border_color="#CBD5E1",
            button_color="#2563EB",
            button_hover_color="#1D4ED8",
            dropdown_hover_color="#DBEAFE",
        )

        self.category_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=8,
        )

        self.category_combo.set("")

        # =========================
        # DESCRIPTION
        # =========================

        description_label = ctk.CTkLabel(
            form,
            text="Description",
            text_color="#374151",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        description_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8,
        )

        self.description_entry = ctk.CTkEntry(
            form,
            placeholder_text="e.g. Lunch",
            height=38,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.description_entry.grid(
            row=2,
            column=1,
            sticky="ew",
            pady=8,
        )

        # =========================
        # DATE
        # =========================

        date_label = ctk.CTkLabel(
            form,
            text="Date",
            text_color="#374151",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        date_label.grid(
            row=3,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8,
        )

        self.date_entry = ctk.CTkEntry(
            form,
            placeholder_text="YYYY-MM-DD",
            height=38,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.date_entry.grid(
            row=3,
            column=1,
            sticky="ew",
            pady=8,
        )

        # Automatically insert today's date
        self.date_entry.insert(
            0,
            date.today().isoformat(),
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
            pady=(0, 5),
        )

        # =========================
        # FORM BUTTONS
        # =========================

        button_frame = ctk.CTkFrame(
            form,
            fg_color="transparent",
        )

        button_frame.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=(15, 0),
        )

        self.save_button = ctk.CTkButton(
            button_frame,
            text="+ Save Expense",
            command=self.save_expense,
            fg_color="#16A34A",
            hover_color="#15803D",
            corner_radius=10,
            height=38,
        )

        self.save_button.pack(
            side="left",
            padx=5,
        )

        clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_form,
            fg_color="#64748B",
            hover_color="#475569",
            corner_radius=10,
            height=38,
        )

        clear_button.pack(
            side="left",
            padx=5,
        )

        # =========================
        # EXPENSE HISTORY CARD
        # =========================

        history_card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="white",
            corner_radius=16,
        )

        history_card.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(10, 25),
        )

        history_title = ctk.CTkLabel(
            history_card,
            text="Expense History",
            text_color="#1F2937",
            font=ctk.CTkFont(
                size=16,
                weight="bold",
            ),
        )

        history_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10),
        )

        # =========================
        # EXPENSE TABLE
        # =========================

        table_frame = ttk.Frame(
            history_card,
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 10),
        )

        columns = (
            "id",
            "amount",
            "category",
            "description",
            "date",
        )

        self.expense_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8,
        )

        self.expense_tree.heading(
            "id",
            text="ID",
        )

        self.expense_tree.heading(
            "amount",
            text="Amount",
        )

        self.expense_tree.heading(
            "category",
            text="Category",
        )

        self.expense_tree.heading(
            "description",
            text="Description",
        )

        self.expense_tree.heading(
            "date",
            text="Date",
        )

        self.expense_tree.column(
            "id",
            width=50,
        )

        self.expense_tree.column(
            "amount",
            width=110,
        )

        self.expense_tree.column(
            "category",
            width=150,
        )

        self.expense_tree.column(
            "description",
            width=260,
        )

        self.expense_tree.column(
            "date",
            width=120,
        )

        # Scrollbar for the table
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.expense_tree.yview,
        )

        self.expense_tree.configure(
            yscrollcommand=scrollbar.set,
        )

        self.expense_tree.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        # =========================
        # HISTORY BUTTONS
        # =========================

        history_buttons = ctk.CTkFrame(
            history_card,
            fg_color="transparent",
        )

        history_buttons.pack(
            pady=(5, 20),
        )

        edit_button = ctk.CTkButton(
            history_buttons,
            text="Edit Selected",
            command=self.edit_selected_expense,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            corner_radius=10,
        )

        edit_button.pack(
            side="left",
            padx=5,
        )

        delete_button = ctk.CTkButton(
            history_buttons,
            text="Delete Selected",
            command=self.delete_selected_expense,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            corner_radius=10,
        )

        delete_button.pack(
            side="left",
            padx=5,
        )

        refresh_button = ctk.CTkButton(
            history_buttons,
            text="Refresh",
            command=self.load_expenses,
            fg_color="#7C3AED",
            hover_color="#6D28D9",
            corner_radius=10,
        )

        refresh_button.pack(
            side="left",
            padx=5,
        )

    # =========================
    # SAVE / UPDATE
    # =========================

    def save_expense(self):
        """Save a new expense or update an existing expense."""

        amount = self.amount_entry.get().strip()
        category = self.category_combo.get().strip()
        description = self.description_entry.get().strip()
        expense_date = self.date_entry.get().strip()

        # Check required fields
        if not amount or not category or not description or not expense_date:
            messagebox.showerror(
                "Missing Fields",
                ("Please enter the amount, category, " "description, and date."),
            )
            return

        # Validate amount
        try:
            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Amount must be greater than zero.",
            )
            return

        # Validate date
        try:
            datetime.strptime(
                expense_date,
                "%Y-%m-%d",
            )

        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Please use YYYY-MM-DD format.",
            )
            return

        # =========================
        # BUDGET CHECK
        # =========================

        budget = get_budget()

        if budget is not None:
            (
                budget_id,
                budget_amount,
                period,
                start_date,
                end_date,
            ) = budget

            # Only compare expenses that belong
            # to the current budget period
            if start_date <= expense_date <= end_date:

                total_spent = get_total_spent(
                    start_date,
                    end_date,
                )

                # If editing an existing expense,
                # remove its old amount before checking
                if self.selected_expense_id is not None:

                    expenses = get_expenses()

                    for existing_expense in expenses:

                        old_id = existing_expense[0]
                        old_amount = existing_expense[1]
                        old_date = existing_expense[4]

                        if old_id == self.selected_expense_id:

                            if start_date <= old_date <= end_date:
                                total_spent -= old_amount

                            break

                remaining_budget = budget_amount - total_spent

                # Warn if this expense exceeds
                # the remaining budget
                if amount > remaining_budget:

                    exceeded_by = amount - remaining_budget

                    continue_anyway = messagebox.askyesno(
                        "Budget Warning",
                        (
                            f"You only have "
                            f"KSh {remaining_budget:,.2f} "
                            f"remaining in your budget.\n\n"
                            f"This expense exceeds your "
                            f"remaining budget by "
                            f"KSh {exceeded_by:,.2f}.\n\n"
                            f"Do you still want to record it?"
                        ),
                    )

                    # User selected No
                    if not continue_anyway:
                        return

        # =========================
        # CREATE EXPENSE OBJECT
        # =========================

        expense = Expense(
            amount=amount,
            category=category,
            description=description,
            date=expense_date,
            expense_id=self.selected_expense_id,
        )

        # Add new expense
        if self.selected_expense_id is None:

            add_expense(expense)

            messagebox.showinfo(
                "Success",
                "Expense added successfully.",
            )

        # Update existing expense
        else:

            update_expense(expense)

            messagebox.showinfo(
                "Success",
                "Expense updated successfully.",
            )

        # Reset and refresh
        self.clear_form()
        self.load_expenses()

        # Refresh dashboard
        if self.on_change:
            self.on_change()

    # =========================
    # READ
    # =========================

    def load_expenses(self):
        """Load expenses from SQLite into the table."""

        # Remove current table rows
        for row in self.expense_tree.get_children():
            self.expense_tree.delete(row)

        expenses = get_expenses()

        for expense in expenses:

            (
                expense_id,
                amount,
                category,
                description,
                expense_date,
            ) = expense

            self.expense_tree.insert(
                "",
                tk.END,
                values=(
                    expense_id,
                    f"KSh {amount:,.2f}",
                    category,
                    description,
                    expense_date,
                ),
            )

    # =========================
    # EDIT
    # =========================

    def edit_selected_expense(self):
        """Load the selected expense into the form."""

        selected = self.expense_tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an expense to edit.",
            )
            return

        values = self.expense_tree.item(
            selected[0],
            "values",
        )

        # Store selected ID
        self.selected_expense_id = int(values[0])

        # Remove KSh from displayed amount
        amount_text = values[1].replace("KSh", "").replace(",", "").strip()

        # Clear current form
        self.clear_entries_only()

        # Put selected values into the form
        self.amount_entry.insert(
            0,
            amount_text,
        )

        self.category_combo.set(values[2])

        self.description_entry.insert(
            0,
            values[3],
        )

        self.date_entry.insert(
            0,
            values[4],
        )

        # Change Save button to Update
        self.save_button.configure(
            text="Update Expense",
            fg_color="#F59E0B",
            hover_color="#D97706",
        )

    # =========================
    # DELETE
    # =========================

    def delete_selected_expense(self):
        """Delete the selected expense."""

        selected = self.expense_tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an expense to delete.",
            )
            return

        values = self.expense_tree.item(
            selected[0],
            "values",
        )

        expense_id = int(values[0])

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?",
        )

        if not confirm:
            return

        delete_expense(expense_id)

        self.clear_form()
        self.load_expenses()

        messagebox.showinfo(
            "Deleted",
            "Expense deleted successfully.",
        )

        if self.on_change:
            self.on_change()

    # =========================
    # CLEAR FORM
    # =========================

    def clear_entries_only(self):
        """Clear all expense form fields."""

        self.amount_entry.delete(
            0,
            tk.END,
        )

        self.category_combo.set("")

        self.description_entry.delete(
            0,
            tk.END,
        )

        self.date_entry.delete(
            0,
            tk.END,
        )

    def clear_form(self):
        """Reset the expense form."""

        self.clear_entries_only()

        # Restore today's date
        self.date_entry.insert(
            0,
            date.today().isoformat(),
        )

        # Stop editing
        self.selected_expense_id = None

        # Restore Save button
        self.save_button.configure(
            text="+ Save Expense",
            fg_color="#16A34A",
            hover_color="#15803D",
        )
