import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from expense_app.analytics.monthly_expenses import plot_monthly_expenses
from expense_app.authentication.auth import get_user_id
from expense_app.authentication.database import (
    add_expense, add_category, get_categories, get_expenses
)
from expense_app.analytics.monthly_expenses import plot_monthly_expenses


class ExpenseUI:
    def __init__(self, username):
        self.user_id = get_user_id(username)

        self.root = tk.Toplevel()
        self.root.title("Expense Manager")

        self.setup_window(width=900, height=600)

        self.container = ttk.Frame(self.root, padding=20)
        self.container.pack(fill="both", expand=True)

        ttk.Label(self.container, text="New Category").pack(pady=5)
        self.new_category = tk.StringVar()
        ttk.Entry(self.container, textvariable=self.new_category).pack()
        ttk.Button(self.container, text="Add Category", command=self.create_category).pack(pady=5)

        ttk.Label(self.container, text="Amount").pack(pady=5)
        self.amount = tk.StringVar()
        ttk.Entry(self.container, textvariable=self.amount).pack()

        ttk.Label(self.container, text="Category").pack(pady=5)
        self.category = tk.StringVar()
        self.category_box = ttk.Combobox(self.container, textvariable=self.category, state="readonly")
        self.category_box.pack()

        ttk.Label(self.container, text="Description").pack(pady=5)
        self.description = tk.StringVar()
        ttk.Entry(self.container, textvariable=self.description).pack()

        ttk.Button(self.container, text="Add Expense", command=self.save_expense).pack(pady=10)

        ttk.Label(self.container, text="Your Expenses").pack(pady=10)
        self.tree = ttk.Treeview(
            self.container,
            columns=("date", "category", "amount", "description"),
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(
            self.container,
            text="View Monthly Expenses",
            command=lambda: plot_monthly_expenses(self.user_id)
        ).pack(pady=10)

        self.refresh_categories()
        self.refresh_expenses()

    def setup_window(self, width=900, height=600):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(width, height)

    def create_category(self):
        name = self.new_category.get().strip()
        if not name:
            return
        add_category(self.user_id, name)
        self.new_category.set("")
        self.refresh_categories()

    def refresh_categories(self):
        categories = get_categories(self.user_id)
        self.category_box["values"] = categories
        if categories:
            self.category_box.current(0)

    def save_expense(self):
        if not self.category.get():
            messagebox.showerror("Error", "Please select a category")
            return

        try:
            amount = float(self.amount.get())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return

        add_expense(
            self.user_id,
            date.today().isoformat(),
            self.category.get(),
            amount,
            self.description.get()
        )

        self.amount.set("")
        self.description.set("")
        self.refresh_expenses()

    def refresh_expenses(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for expense in get_expenses(self.user_id):
            self.tree.insert("", "end", values=expense)

