import customtkinter as ctk
from tkinter import messagebox

from database import (
    create_user,
    authenticate_user,
)


class AuthFrame(ctk.CTkFrame):
    """Login and account creation screen."""

    def __init__(self, parent, on_login_success):
        super().__init__(
            parent,
            fg_color="#F4F7FB",
            corner_radius=0,
        )

        self.on_login_success = on_login_success

        self.pack(
            fill="both",
            expand=True,
        )

        self.create_widgets()

    def create_widgets(self):
        """Create the authentication interface."""

        # =========================
        # MAIN CONTAINER
        # =========================

        main_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25,
        )

        main_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        main_frame.grid_columnconfigure(
            1,
            weight=1,
        )

        main_frame.grid_rowconfigure(
            0,
            weight=1,
        )

        # =========================
        # LEFT SIDE - APP INFO
        # =========================

        info_frame = ctk.CTkFrame(
            main_frame,
            fg_color="#2563EB",
            corner_radius=20,
        )

        info_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8),
        )

        app_icon = ctk.CTkLabel(
            info_frame,
            text="💰",
            font=ctk.CTkFont(
                size=42,
            ),
        )

        app_icon.pack(
            anchor="w",
            padx=30,
            pady=(45, 12),
        )

        title = ctk.CTkLabel(
            info_frame,
            text="Campus Money Manager",
            text_color="white",
            font=ctk.CTkFont(
                size=25,
                weight="bold",
            ),
        )

        title.pack(
            anchor="w",
            padx=30,
        )

        subtitle = ctk.CTkLabel(
            info_frame,
            text=(
                "A simple budgeting tool designed to help "
                "students manage their money better."
            ),
            text_color="#DBEAFE",
            font=ctk.CTkFont(
                size=12,
            ),
            wraplength=320,
            justify="left",
        )

        subtitle.pack(
            anchor="w",
            padx=30,
            pady=(10, 25),
        )

        features = (
            "✓ Track your daily expenses\n\n"
            "✓ Set weekly or monthly budgets\n\n"
            "✓ Monitor your daily allowance\n\n"
            "✓ Plan purchases before spending"
        )

        feature_label = ctk.CTkLabel(
            info_frame,
            text=features,
            text_color="white",
            font=ctk.CTkFont(
                size=12,
            ),
            justify="left",
        )

        feature_label.pack(
            anchor="w",
            padx=30,
            pady=(0, 30),
        )

        # =========================
        # RIGHT SIDE - AUTH CARD
        # =========================

        auth_card = ctk.CTkFrame(
            main_frame,
            fg_color="white",
            corner_radius=20,
        )

        auth_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0),
        )

        auth_title = ctk.CTkLabel(
            auth_card,
            text="Welcome",
            text_color="#1F2937",
            font=ctk.CTkFont(
                size=23,
                weight="bold",
            ),
        )

        auth_title.pack(
            pady=(25, 5),
        )

        auth_subtitle = ctk.CTkLabel(
            auth_card,
            text="Log in or create an account to continue.",
            text_color="#6B7280",
            font=ctk.CTkFont(
                size=11,
            ),
        )

        auth_subtitle.pack(
            pady=(0, 15),
        )

        # =========================
        # LOGIN / CREATE TABS
        # =========================

        self.auth_tabs = ctk.CTkTabview(
            auth_card,
            fg_color="#F8FAFC",
            segmented_button_selected_color="#2563EB",
            segmented_button_selected_hover_color="#1D4ED8",
            segmented_button_unselected_hover_color="#DBEAFE",
        )

        self.auth_tabs.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20),
        )

        self.auth_tabs.add(
            "Login"
        )

        self.auth_tabs.add(
            "Create Account"
        )

        self.create_login_tab()
        self.create_signup_tab()

    # =========================
    # LOGIN TAB
    # =========================

    def create_login_tab(self):
        """Create the login form."""

        login_tab = self.auth_tabs.tab(
            "Login"
        )

        # Scrollable so the form works on smaller screens
        login_scroll = ctk.CTkScrollableFrame(
            login_tab,
            fg_color="transparent",
            corner_radius=0,
        )

        login_scroll.pack(
            fill="both",
            expand=True,
        )

        login_title = ctk.CTkLabel(
            login_scroll,
            text="Log In",
            text_color="#1F2937",
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        )

        login_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5),
        )

        login_text = ctk.CTkLabel(
            login_scroll,
            text="Enter your account details.",
            text_color="#6B7280",
            font=ctk.CTkFont(
                size=11,
            ),
        )

        login_text.pack(
            anchor="w",
            padx=20,
            pady=(0, 18),
        )

        # Username label
        username_label = ctk.CTkLabel(
            login_scroll,
            text="Username",
            text_color="#374151",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        username_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 5),
        )

        # Username entry
        self.login_username_entry = ctk.CTkEntry(
            login_scroll,
            placeholder_text="Enter username",
            height=40,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.login_username_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 15),
        )

        # Password label
        password_label = ctk.CTkLabel(
            login_scroll,
            text="Password",
            text_color="#374151",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        password_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 5),
        )

        # Password entry
        self.login_password_entry = ctk.CTkEntry(
            login_scroll,
            placeholder_text="Enter password",
            show="•",
            height=40,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.login_password_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 20),
        )

        # Login button
        login_button = ctk.CTkButton(
            login_scroll,
            text="Log In",
            command=self.login,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            height=40,
            corner_radius=10,
        )

        login_button.pack(
            fill="x",
            padx=20,
            pady=(0, 30),
        )

        # Pressing Enter also logs in
        self.login_password_entry.bind(
            "<Return>",
            lambda event: self.login(),
        )

    # =========================
    # CREATE ACCOUNT TAB
    # =========================

    def create_signup_tab(self):
        """Create the account registration form."""

        signup_tab = self.auth_tabs.tab(
            "Create Account"
        )

        # Scrollable so the button remains reachable
        signup_scroll = ctk.CTkScrollableFrame(
            signup_tab,
            fg_color="transparent",
            corner_radius=0,
        )

        signup_scroll.pack(
            fill="both",
            expand=True,
        )

        signup_title = ctk.CTkLabel(
            signup_scroll,
            text="Create Account",
            text_color="#1F2937",
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        )

        signup_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5),
        )

        signup_text = ctk.CTkLabel(
            signup_scroll,
            text="Create an account to start managing your money.",
            text_color="#6B7280",
            font=ctk.CTkFont(
                size=11,
            ),
        )

        signup_text.pack(
            anchor="w",
            padx=20,
            pady=(0, 18),
        )

        # Username label
        username_label = ctk.CTkLabel(
            signup_scroll,
            text="Username",
            text_color="#374151",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        username_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 5),
        )

        # Username entry
        self.signup_username_entry = ctk.CTkEntry(
            signup_scroll,
            placeholder_text="Choose a username",
            height=40,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.signup_username_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 15),
        )

        # Password label
        password_label = ctk.CTkLabel(
            signup_scroll,
            text="Password",
            text_color="#374151",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        password_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 5),
        )

        # Password entry
        self.signup_password_entry = ctk.CTkEntry(
            signup_scroll,
            placeholder_text="Create a password",
            show="•",
            height=40,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.signup_password_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 15),
        )

        # Confirm password label
        confirm_label = ctk.CTkLabel(
            signup_scroll,
            text="Confirm Password",
            text_color="#374151",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )

        confirm_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 5),
        )

        # Confirm password entry
        self.confirm_password_entry = ctk.CTkEntry(
            signup_scroll,
            placeholder_text="Enter password again",
            show="•",
            height=40,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.confirm_password_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 20),
        )

        # Create Account button
        signup_button = ctk.CTkButton(
            signup_scroll,
            text="Create Account",
            command=self.signup,
            fg_color="#16A34A",
            hover_color="#15803D",
            height=40,
            corner_radius=10,
        )

        signup_button.pack(
            fill="x",
            padx=20,
            pady=(0, 35),
        )

    # =========================
    # LOGIN LOGIC
    # =========================

    def login(self):
        """Log an existing user into the application."""

        username = (
            self.login_username_entry
            .get()
            .strip()
        )

        password = (
            self.login_password_entry
            .get()
        )

        # Make sure both fields are filled
        if not username or not password:
            messagebox.showerror(
                "Missing Information",
                "Please enter your username and password.",
            )
            return

        # Check login details
        user = authenticate_user(
            username,
            password,
        )

        # Login failed
        if user is None:
            messagebox.showerror(
                "Login Failed",
                "Incorrect username or password.",
            )
            return

        # Login successful
        self.on_login_success(
            user
        )

    # =========================
    # SIGNUP LOGIC
    # =========================

    def signup(self):
        """Create a new user account."""

        username = (
            self.signup_username_entry
            .get()
            .strip()
        )

        password = (
            self.signup_password_entry
            .get()
        )

        confirm_password = (
            self.confirm_password_entry
            .get()
        )

        # Make sure all fields are filled
        if (
            not username
            or not password
            or not confirm_password
        ):
            messagebox.showerror(
                "Missing Information",
                "Please complete all fields.",
            )
            return

        # Username validation
        if len(username) < 3:
            messagebox.showerror(
                "Invalid Username",
                "Username must contain at least 3 characters.",
            )
            return

        # Password validation
        if len(password) < 6:
            messagebox.showerror(
                "Weak Password",
                "Password must contain at least 6 characters.",
            )
            return

        # Confirm passwords match
        if password != confirm_password:
            messagebox.showerror(
                "Passwords Do Not Match",
                "Please enter the same password twice.",
            )
            return

        # Create the account
        success, result = create_user(
            username,
            password,
        )

        if not success:
            messagebox.showerror(
                "Account Not Created",
                result,
            )
            return

        messagebox.showinfo(
            "Account Created",
            (
                "Your account was created successfully.\n\n"
                "You can now log in."
            ),
        )

        # Clear signup fields
        self.signup_username_entry.delete(
            0,
            "end",
        )

        self.signup_password_entry.delete(
            0,
            "end",
        )

        self.confirm_password_entry.delete(
            0,
            "end",
        )

        # Switch back to Login
        self.auth_tabs.set(
            "Login"
        )

        # Automatically copy username to login form
        self.login_username_entry.delete(
            0,
            "end",
        )

        self.login_username_entry.insert(
            0,
            username,
        )

        # Move cursor to password field
        self.login_password_entry.focus()