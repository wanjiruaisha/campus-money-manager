from tkinter import ttk

from database import set_current_user

from .auth import AuthFrame
from .dashboard import DashboardFrame
from .expenses import ExpenseFrame
from .budget import BudgetFrame
from .affordability import AffordabilityFrame


class CampusMoneyApp:
    """Main graphical interface for Campus Money Manager."""

    def __init__(self, root):
        self.root = root

        self.root.title("Campus Money Manager")

        self.root.geometry("1000x650")

        self.root.minsize(850, 550)

        self.root.configure(fg_color="#F4F7FB")

        # Stores the currently logged-in user
        self.current_user = None

        # These are created after login
        self.notebook = None
        self.dashboard_frame = None
        self.expense_frame = None
        self.budget_frame = None
        self.affordability_frame = None

        # Show authentication screen first
        self.show_auth()

    # =========================
    # AUTHENTICATION
    # =========================

    def show_auth(self):
        """Display the login/create account screen."""

        # Remove anything currently displayed
        self.clear_root()

        self.auth_frame = AuthFrame(
            self.root,
            on_login_success=self.login_success,
        )

    def login_success(self, user):
        """Handle a successful login."""

        self.current_user = user

        # Tell the database which user is logged in
        set_current_user(user["id"])

        self.show_main_app()

    # =========================
    # MAIN APPLICATION
    # =========================

    def show_main_app(self):
        """Display the application after login."""

        self.clear_root()

        # =========================
        # TOP BAR
        # =========================

        top_bar = ttk.Frame(self.root)

        top_bar.pack(
        fill="x",
        padx=10,
        pady=(10, 0),
        )

        # Show logged-in username
        user_label = ttk.Label(
        top_bar,
        text=f"Logged in as: {self.current_user['username']}",
        )

        user_label.pack(
        side="left",
        padx=10,
        pady=5,
        )

        # Logout button
        logout_button = ttk.Button(
        top_bar,
        text="Logout",
        command=self.logout,
        )

        logout_button.pack(
        side="right",
        padx=10,
        pady=5,
        )


        

        # Create Notebook navigation
        self.notebook = ttk.Notebook(self.root)

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10,
        )

        # Dashboard
        self.dashboard_frame = DashboardFrame(self.notebook)

        # Expenses
        self.expense_frame = ExpenseFrame(
            self.notebook,
            on_change=self.refresh_data,
        )

        # Budget
        self.budget_frame = BudgetFrame(
            self.notebook,
            on_change=self.refresh_data,
        )

        # Purchase Planner
        self.affordability_frame = AffordabilityFrame(self.notebook)

        # Add tabs
        self.notebook.add(
            self.dashboard_frame,
            text="Dashboard",
        )

        self.notebook.add(
            self.expense_frame,
            text="Expenses",
        )

        self.notebook.add(
            self.budget_frame,
            text="Budget",
        )

        self.notebook.add(
            self.affordability_frame,
            text="Purchase Planner",
        )

        # Detect tab changes
        self.notebook.bind(
            "<<NotebookTabChanged>>",
            self.on_tab_changed,
        )

    # =========================
    # REFRESH DATA
    # =========================

    def refresh_data(self):
        """Refresh screens after data changes."""

        if self.dashboard_frame:
            self.dashboard_frame.refresh()

        if self.expense_frame:
            self.expense_frame.load_expenses()

    def on_tab_changed(self, event):
        """Refresh data when switching tabs."""

        selected_tab = self.notebook.index(self.notebook.select())

        # Dashboard
        if selected_tab == 0:
            self.dashboard_frame.refresh()

        # Expenses
        elif selected_tab == 1:
            self.expense_frame.load_expenses()

        # Budget
        elif selected_tab == 2:
            self.budget_frame.load_budget()

    # =========================
    # CLEAR WINDOW
    # =========================

    def clear_root(self):
        """Remove all widgets from the main window."""

        for widget in self.root.winfo_children():
            widget.destroy()

    # =========================
    # LOGOUT FUNCTION
    # =========================

    def logout(self):
        """Log the current user out."""

        self.current_user = None

        # Clear the active user from the database
        set_current_user(None)

        # Return to login screen
        self.show_auth()