import tkinter as tk
from style import apply_style
from expense_app.authentication.database import setup_databse
from expense_app.authentication.ui_auth import AuthUI
from expense_app.expenses.ui_expenses import ExpenseUI
from expense_app.authentication.database import (
    setup_expense_tables, setup_category_table
)


def launch_main_app(username):
    setup_expense_tables()
    setup_category_table()
    ExpenseUI(username)

if __name__ == "__main__":
    setup_databse()
    root = tk.Tk()
    apply_style(root)
    root.state('zoomed')
    AuthUI(root, launch_main_app)
    root.mainloop()
