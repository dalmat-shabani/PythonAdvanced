import sqlite3
from typing import Iterator
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "recipes.db")

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(""" CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
    );""")


    cur.execute(""" CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT ,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    cuisine TEXT,
    difficulty TEXT,
    category INTEGER ,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
    );""")

    conn.commit()
    conn.close()