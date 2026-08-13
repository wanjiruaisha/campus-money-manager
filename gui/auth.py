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

        # Main container
        main_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        main_frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=40,
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
            padx=(0, 10),
        )

        app_icon = ctk.CTkLabel(
            info_frame,
            text="💰",
            font=ctk.CTkFont(
                size=45,
            ),
        )

        app_icon.pack(
            anchor="w",
            padx=35,
            pady=(60, 15),
        )

        title = ctk.CTkLabel(
            info_frame,
            text="Campus Money Manager",
            text_color="white",
            font=ctk.CTkFont(
                size=27,
                weight="bold",
            ),
        )

        title.pack(
            anchor="w",
            padx=35,
        )

        subtitle = ctk.CTkLabel(
            info_frame,
            text=(
                "A simple budgeting tool designed to help "
                "students manage their money better."
            ),
            text_color="#DBEAFE",
            font=ctk.CTkFont(
                size=13,
            ),
            wraplength=350,
            justify="left",
        )

        subtitle.pack(
            anchor="w",
            padx=35,
            pady=(10, 30),
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
                size=13,
            ),
            justify="left",
        )

        feature_label.pack(
            anchor="w",
            padx=35,
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
            padx=(10, 0),
        )

        auth_title = ctk.CTkLabel(
            auth_card,
            text="Welcome",
            text_color="#1F2937",
            font=ctk.CTkFont(
                size=24,
                weight="bold",
            ),
        )

        auth_title.pack(
            pady=(45, 5),
        )

        auth_subtitle = ctk.CTkLabel(
            auth_card,
            text="Log in or create an account to continue.",
            text_color="#6B7280",
            font=ctk.CTkFont(
                size=12,
            ),
        )

        auth_subtitle.pack(
            pady=(0, 20),
        )

        # Tabs for Login and Sign Up
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
            padx=30,
            pady=(0, 30),
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
        """Create login form."""

        login_tab = self.auth_tabs.tab(
            "Login"
        )

        login_title = ctk.CTkLabel(
            login_tab,
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
            pady=(25, 5),
        )

        login_text = ctk.CTkLabel(
            login_tab,
            text="Enter your account details.",
            text_color="#6B7280",
            font=ctk.CTkFont(
                size=11,
            ),
        )

        login_text.pack(
            anchor="w",
            padx=20,
            pady=(0, 20),
        )

        # Username
        username_label = ctk.CTkLabel(
            login_tab,
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

        self.login_username_entry = ctk.CTkEntry(
            login_tab,
            placeholder_text="Enter username",
            height=42,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.login_username_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 15),
        )

        # Password
        password_label = ctk.CTkLabel(
            login_tab,
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

        self.login_password_entry = ctk.CTkEntry(
            login_tab,
            placeholder_text="Enter password",
            show="•",
            height=42,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.login_password_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 20),
        )

        login_button = ctk.CTkButton(
            login_tab,
            text="Log In",
            command=self.login,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            height=42,
            corner_radius=10,
        )

        login_button.pack(
            fill="x",
            padx=20,
            pady=(0, 20),
        )

        # Allow Enter key to log in
        self.login_password_entry.bind(
            "<Return>",
            lambda event: self.login(),
        )

    # =========================
    # CREATE ACCOUNT TAB
    # =========================

    def create_signup_tab(self):
        """Create account registration form."""

        signup_tab = self.auth_tabs.tab(
            "Create Account"
        )

        signup_title = ctk.CTkLabel(
            signup_tab,
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
            pady=(25, 5),
        )

        signup_text = ctk.CTkLabel(
            signup_tab,
            text="Create an account to start managing your money.",
            text_color="#6B7280",
            font=ctk.CTkFont(
                size=11,
            ),
        )

        signup_text.pack(
            anchor="w",
            padx=20,
            pady=(0, 20),
        )

        # Username
        username_label = ctk.CTkLabel(
            signup_tab,
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

        self.signup_username_entry = ctk.CTkEntry(
            signup_tab,
            placeholder_text="Choose a username",
            height=42,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.signup_username_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 15),
        )

        # Password
        password_label = ctk.CTkLabel(
            signup_tab,
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

        self.signup_password_entry = ctk.CTkEntry(
            signup_tab,
            placeholder_text="Create a password",
            show="•",
            height=42,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.signup_password_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 15),
        )

        # Confirm password
        confirm_label = ctk.CTkLabel(
            signup_tab,
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

        self.confirm_password_entry = ctk.CTkEntry(
            signup_tab,
            placeholder_text="Enter password again",
            show="•",
            height=42,
            corner_radius=10,
            border_color="#CBD5E1",
        )

        self.confirm_password_entry.pack(
            fill="x",
            padx=20,
            pady=(0, 20),
        )

        signup_button = ctk.CTkButton(
            signup_tab,
            text="Create Account",
            command=self.signup,
            fg_color="#16A34A",
            hover_color="#15803D",
            height=42,
            corner_radius=10,
        )

        signup_button.pack(
            fill="x",
            padx=20,
            pady=(0, 20),
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

        # Make sure fields are filled
        if not username or not password:
            messagebox.showerror(
                "Missing Information",
                "Please enter your username and password.",
            )
            return

        # Check credentials
        user = authenticate_user(
            username,
            password,
        )

        if user is None:
            messagebox.showerror(
                "Login Failed",
                "Incorrect username or password.",
            )
            return

        # Login succeeded
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

        # Check required fields
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

        # Username must have at least 3 characters
        if len(username) < 3:
            messagebox.showerror(
                "Invalid Username",
                "Username must contain at least 3 characters.",
            )
            return

        # Password must have at least 6 characters
        if len(password) < 6:
            messagebox.showerror(
                "Weak Password",
                "Password must contain at least 6 characters.",
            )
            return

        # Make sure passwords match
        if password != confirm_password:
            messagebox.showerror(
                "Passwords Do Not Match",
                "Please enter the same password twice.",
            )
            return

        # Create account
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

        # Clear signup form
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

        # Move user to Login tab
        self.auth_tabs.set(
            "Login"
        )

        # Automatically place username
        # into login field
        self.login_username_entry.delete(
            0,
            "end",
        )

        self.login_username_entry.insert(
            0,
            username,
        )

        # Focus password field
        self.login_password_entry.focus()