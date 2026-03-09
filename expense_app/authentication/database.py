import sqlite3

def get_connection():
    return sqlite3.connect('app.db')

def setup_databse():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def setup_expense_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()

def setup_category_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        UNIQUE (user_id, name),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ''')

    conn.commit()
    conn.close()


def setup_budget_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        monthly_budget REAL NOT NULL,
        UNIQUE (user_id, category),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ''')

    conn.commit()
    conn.close()

def add_expense(user_id, date, category, amount, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO expenses (user_id, date, category, amount, description)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, date, category, amount, description))

    conn.commit()
    conn.close()

def add_category(user_id, name):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO categories (user_id, name) VALUES (?, ?)",
            (user_id, name)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()


def set_budget(user_id, category, monthly_budget):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO budgets (user_id, category, monthly_budget)
    VALUES (?, ?, ?)
    ON CONFLICT(user_id, category)
    DO UPDATE SET monthly_budget = excluded.monthly_budget
    ''', (user_id, category, monthly_budget))

    conn.commit()
    conn.close()


def get_budgets(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT category, monthly_budget FROM budgets WHERE user_id = ?",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_categories(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM categories WHERE user_id = ?",
        (user_id,)
    )

    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

def get_expenses(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT date, category, amount, description 
    FROM expenses 
    WHERE user_id = ? 
    ORDER BY date ASC
    ''', (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expenses_with_ids(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT id, date, category, amount, description
        FROM expenses
        WHERE user_id = ?
        ORDER BY date ASC
        ''',
        (user_id,),
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expense_by_id(user_id, expense_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT id, date, category, amount, description
        FROM expenses
        WHERE user_id = ? AND id = ?
        ''',
        (user_id, expense_id),
    )
    row = cursor.fetchone()
    conn.close()
    return row


def update_expense(user_id, expense_id, date_value, category, amount, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        '''
        UPDATE expenses
        SET date = ?, category = ?, amount = ?, description = ?
        WHERE user_id = ? AND id = ?
        ''',
        (date_value, category, amount, description, user_id, expense_id),
    )

    conn.commit()
    conn.close()


def delete_expense(user_id, expense_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'DELETE FROM expenses WHERE user_id = ? AND id = ?',
        (user_id, expense_id),
    )

    conn.commit()
    conn.close()

def get_user_id(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,)
    )
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None