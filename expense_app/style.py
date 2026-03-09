import tkinter as tk
from tkinter import ttk

BG = "#F7F8F0"
PRIMARY = "#355872"
ACCENT = "#7AAACE"
SECONDARY = "#9CD5FF"
TEXT = "#000000"

def apply_style(root):
    root.configure(bg=BG)

    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(
        "TLabel",
        background=BG,
        foreground=TEXT,
        font=("Segoe UI", 11)
    )

    style.configure(
        "TButton",
        background=PRIMARY,
        foreground=BG,
        font=("Segoe UI", 10),
        padding=6
    )
    style.map(
        "TButton",
        background=[("active", ACCENT)]
    )

    style.configure(
        "TEntry",
        fieldbackground=SECONDARY,
        foreground=TEXT,
        padding=4
    )

    style.configure(
        "TCombobox",
        fieldbackground=SECONDARY,
        foreground=TEXT
    )