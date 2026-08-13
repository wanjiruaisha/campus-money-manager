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

        # Main background colour
        self.root.configure(bg="#F4F7FB")

        # Apply application colours
        self.configure_styles()

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
             text="Purchase Planner"
        )
        # Refresh data when switching tabs
        self.notebook.bind(
            "<<NotebookTabChanged>>",
            self.on_tab_changed
        )

    def configure_styles(self):
        """Configure colours and styles for the application."""

        style = ttk.Style()

        # Clam allows more colour customization
        style.theme_use("clam")

        # Main frames
        style.configure(
            "TFrame",
            background="#F4F7FB"
        )

        # Normal labels
        style.configure(
            "TLabel",
            background="#F4F7FB",
            foreground="#1F2937",
            font=("Arial", 10)
        )

        # Label frames / sections
        style.configure(
            "TLabelframe",
            background="#FFFFFF",
            borderwidth=1,
            relief="solid"
        )

        style.configure(
            "TLabelframe.Label",
            background="#FFFFFF",
            foreground="#1F2937",
            font=("Arial", 11, "bold")
        )

        # Buttons
        style.configure(
            "TButton",
            background="#2563EB",
            foreground="white",
            padding=(12, 7),
            font=("Arial", 10, "bold"),
            borderwidth=0
        )

        # Button hover effect
        style.map(
            "TButton",
            background=[
                ("active", "#1D4ED8")
            ],
            foreground=[
                ("active", "white")
            ]
        )

        # Red delete button
        style.configure(
            "Danger.TButton",
            background="#DC2626",
            foreground="white"
        )

        style.map(
            "Danger.TButton",
            background=[
                ("active", "#B91C1C")
            ]
        )

        # Green button
        style.configure(
            "Success.TButton",
            background="#16A34A",
            foreground="white"
        )

        style.map(
            "Success.TButton",
            background=[
                ("active", "#15803D")
            ]
        )

        # Text entry fields
        style.configure(
            "TEntry",
            fieldbackground="#FFFFFF",
            foreground="#1F2937",
            padding=6
        )

        # Dropdowns
        style.configure(
            "TCombobox",
            fieldbackground="#FFFFFF",
            foreground="#1F2937",
            padding=5
        )

        # Expense tables
        style.configure(
            "Treeview",
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground="#1F2937",
            rowheight=28,
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#2563EB",
            foreground="white",
            font=("Arial", 10, "bold")
        )

        style.map(
            "Treeview.Heading",
            background=[
                ("active", "#1D4ED8")
            ]
        )

        # Navigation tabs
        style.configure(
            "TNotebook",
            background="#F4F7FB",
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            background="#E5E7EB",
            foreground="#374151",
            padding=(15, 8),
            font=("Arial", 10, "bold")
        )

        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", "#2563EB")
            ],
            foreground=[
                ("selected", "white")
            ]
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

        if selected_tab == 0:
            self.dashboard_frame.refresh()

        elif selected_tab == 1:
            self.expense_frame.load_expenses()

        elif selected_tab == 2:
            self.budget_frame.load_budget()