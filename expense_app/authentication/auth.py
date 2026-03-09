import hashlib
from expense_app.authentication.database import get_connection


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def signup(username, password):
    if not username or not password:
        return False, "All fields are required"

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True, "Account created successfully"
    except:
        return False, "Username already exists"
    finally:
        conn.close()


def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password_hash FROM users WHERE username = ?",
        (username,)
    )
    result = cursor.fetchone()
    conn.close()

    if not result:
        return False, "User not found"

    if result[0] == hash_password(password):
        return True, "Login successful"
    return False, "Incorrect password"

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