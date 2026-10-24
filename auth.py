import sqlite3
from database import get_connection

def verify_login(choice: int, identifier: str, password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if choice != 1 and choice != 2:
            return False
    
        if choice == 1:
            cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?", (identifier, password)
            )
            row = cursor.fetchone()
            return row is not None

        if choice == 2:
            cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?", (identifier, password)
            )
            row = cursor.fetchone()
            return row is not None
    finally:
        conn.close()


def register_user(username: str, email: str, password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
    (username, email, password),
)
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()