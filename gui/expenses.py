import tkinter as tk

from tkinter import (
    ttk,
    messagebox
)

from datetime import (
    date,
    datetime
)

from models import Expense

from database import (
    add_expense,
    get_expenses,
    update_expense,
    delete_expense
)


class ExpenseFrame(ttk.Frame):
    """Screen used to manage expenses."""

    def __init__(
        self,
        parent,
        on_change=None
    ):
        super().__init__(parent)

        self.on_change = on_change

        # ID of expense currently being edited
        self.selected_expense_id = None

        self.create_widgets()
        self.load_expenses()

    def create_widgets(self):
        """Create expense form and history table."""

        title = ttk.Label(
            self,
            text="Expense Management",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=20)

        # ---------------- FORM ----------------

        form = ttk.LabelFrame(
            self,
            text="Expense Details",
            padding=15
        )

        form.pack(
            fill="x",
            padx=25,
            pady=10
        )

        form.columnconfigure(
            1,
            weight=1
        )

        # Amount
        ttk.Label(
            form,
            text="Amount:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=8
        )

        self.amount_entry = ttk.Entry(
            form
        )

        self.amount_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=10,
            pady=8
        )

        # Category
        ttk.Label(
            form,
            text="Category:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=10,
            pady=8
        )

        self.category_combo = ttk.Combobox(
            form,
            state="readonly"
        )

        self.category_combo["values"] = (
            "Food",
            "Transport",
            "School",
            "Printing",
            "Airtime and Data",
            "Entertainment",
            "Personal Expenses",
            "Other"
        )

        self.category_combo.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=10,
            pady=8
        )

        # Description
        ttk.Label(
            form,
            text="Description:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=10,
            pady=8
        )

        self.description_entry = ttk.Entry(
            form
        )

        self.description_entry.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=10,
            pady=8
        )

        # Date
        ttk.Label(
            form,
            text="Date:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=10,
            pady=8
        )

        self.date_entry = ttk.Entry(
            form
        )

        self.date_entry.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=10,
            pady=8
        )

        self.date_entry.insert(
            0,
            date.today().isoformat()
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

        # Form buttons
        button_frame = ttk.Frame(
            form
        )

        button_frame.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=15
        )

        self.save_button = ttk.Button(
            button_frame,
            text="Save Expense",
            command=self.save_expense
        )

        self.save_button.pack(
            side="left",
            padx=5
        )

        clear_button = ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_form
        )

        clear_button.pack(
            side="left",
            padx=5
        )

        # ---------------- HISTORY ----------------

        history_frame = ttk.LabelFrame(
            self,
            text="Expense History",
            padding=10
        )

        history_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=15
        )

        columns = (
            "id",
            "amount",
            "category",
            "description",
            "date"
        )

        self.expense_tree = ttk.Treeview(
            history_frame,
            columns=columns,
            show="headings"
        )

        self.expense_tree.heading(
            "id",
            text="ID"
        )

        self.expense_tree.heading(
            "amount",
            text="Amount"
        )

        self.expense_tree.heading(
            "category",
            text="Category"
        )

        self.expense_tree.heading(
            "description",
            text="Description"
        )

        self.expense_tree.heading(
            "date",
            text="Date"
        )

        self.expense_tree.column(
            "id",
            width=50
        )

        self.expense_tree.column(
            "amount",
            width=100
        )

        self.expense_tree.column(
            "category",
            width=150
        )

        self.expense_tree.column(
            "description",
            width=250
        )

        self.expense_tree.column(
            "date",
            width=120
        )

        scrollbar = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.expense_tree.yview
        )

        self.expense_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.expense_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # History buttons
        history_buttons = ttk.Frame(
            self
        )

        history_buttons.pack(
            pady=(0, 15)
        )

        edit_button = ttk.Button(
            history_buttons,
            text="Edit Selected",
            command=self.edit_selected_expense
        )

        edit_button.pack(
            side="left",
            padx=5
        )

        delete_button = ttk.Button(
            history_buttons,
            text="Delete Selected",
            command=self.delete_selected_expense
        )

        delete_button.pack(
            side="left",
            padx=5
        )

        refresh_button = ttk.Button(
            history_buttons,
            text="Refresh",
            command=self.load_expenses
        )

        refresh_button.pack(
            side="left",
            padx=5
        )

    def save_expense(self):
        """Save or update an expense."""

        amount = self.amount_entry.get().strip()
        category = self.category_combo.get().strip()
        description = self.description_entry.get().strip()
        expense_date = self.date_entry.get().strip()

        # Check required fields
        if not amount or not category or not expense_date:
            messagebox.showerror(
                "Missing Information",
                "Please enter the amount, category and date."
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
                "Amount must be greater than zero."
            )
            return

        # Validate date
        try:
            datetime.strptime(
                expense_date,
                "%Y-%m-%d"
            )

        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Please use YYYY-MM-DD format."
            )
            return

        expense = Expense(
            amount=amount,
            category=category,
            description=description,
            date=expense_date,
            expense_id=self.selected_expense_id
        )

        # Add new expense
        if self.selected_expense_id is None:

            add_expense(expense)

            messagebox.showinfo(
                "Success",
                "Expense added successfully."
            )

        # Update existing expense
        else:

            update_expense(expense)

            messagebox.showinfo(
                "Success",
                "Expense updated successfully."
            )

        self.clear_form()
        self.load_expenses()

        if self.on_change:
            self.on_change()

    def load_expenses(self):
        """Load expenses from SQLite."""

        for row in self.expense_tree.get_children():
            self.expense_tree.delete(row)

        expenses = get_expenses()

        for expense in expenses:

            expense_id, amount, category, description, expense_date = expense

            self.expense_tree.insert(
                "",
                tk.END,
                values=(
                    expense_id,
                    f"{amount:.2f}",
                    category,
                    description,
                    expense_date
                )
            )

    def edit_selected_expense(self):
        """Load an expense into the form for editing."""

        selected = self.expense_tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an expense to edit."
            )
            return

        values = self.expense_tree.item(
            selected[0],
            "values"
        )

        self.selected_expense_id = int(
            values[0]
        )

        self.clear_entries_only()

        self.amount_entry.insert(
            0,
            values[1]
        )

        self.category_combo.set(
            values[2]
        )

        self.description_entry.insert(
            0,
            values[3]
        )

        self.date_entry.insert(
            0,
            values[4]
        )

        self.save_button.config(
            text="Update Expense"
        )

    def delete_selected_expense(self):
        """Delete the selected expense."""

        selected = self.expense_tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an expense to delete."
            )
            return

        values = self.expense_tree.item(
            selected[0],
            "values"
        )

        expense_id = int(
            values[0]
        )

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?"
        )

        if not confirm:
            return

        delete_expense(
            expense_id
        )

        self.clear_form()
        self.load_expenses()

        messagebox.showinfo(
            "Deleted",
            "Expense deleted successfully."
        )

        if self.on_change:
            self.on_change()

    def clear_entries_only(self):
        """Clear expense fields."""

        self.amount_entry.delete(
            0,
            tk.END
        )

        self.category_combo.set("")

        self.description_entry.delete(
            0,
            tk.END
        )

        self.date_entry.delete(
            0,
            tk.END
        )

    def clear_form(self):
        """Reset the expense form."""

        self.clear_entries_only()

        self.date_entry.insert(
            0,
            date.today().isoformat()
        )

        self.selected_expense_id = None

        self.save_button.config(
            text="Save Expense"
        )