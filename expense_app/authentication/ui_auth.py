import tkinter as tk
from tkinter import ttk
from expense_app.authentication.auth import signup, login


class AuthUI:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("Expense Manager - Login")

        self.setup_window(width=800, height=500)

        self.container = ttk.Frame(self.root, padding=30)
        self.container.pack(fill="both", expand=True)

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.message = tk.StringVar()

        ttk.Label(
            self.container,
            textvariable=self.message,
            foreground="#355872",  # palette color
            font=("Segoe UI", 10)
        ).pack(pady=(0, 10))

        ttk.Label(self.container, text="Username").pack(pady=(5, 0))
        ttk.Entry(self.container, textvariable=self.username, font=("Segoe UI", 12)).pack(fill="x", pady=5)

        ttk.Label(self.container, text="Password").pack(pady=(10, 0))
        ttk.Entry(self.container, textvariable=self.password, show="*", font=("Segoe UI", 12)).pack(fill="x", pady=5)

        ttk.Button(self.container, text="Login", command=self.handle_login).pack(pady=15, fill="x")
        ttk.Button(self.container, text="Sign Up", command=self.handle_signup).pack(pady=5, fill="x")

    def setup_window(self, width=800, height=500):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(width, height)

    def handle_login(self):
        success, msg = login(self.username.get(), self.password.get())
        if success:
            self.message.set("Login successful ✔")
            self.root.destroy()
            self.on_success(self.username.get())
        else:
            self.message.set(f"Login Failed: {msg}")

    def handle_signup(self):
        success, msg = signup(self.username.get(), self.password.get())
        if success:
            self.message.set("Sign Up successful ✔")
        else:
            self.message.set(f"Sign Up Failed: {msg}")
