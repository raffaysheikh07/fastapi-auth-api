import sqlite3, bcrypt
from pydantic import Field
from database import get_connection

def verify_login(identifier: str, password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
        "SELECT password FROM users WHERE (username = ? OR email = ?)", (identifier, identifier)
        )
        row = cursor.fetchone()
        if row is None:
            return False
        return bcrypt.checkpw(password.encode(),row[0].encode())
    finally:
        conn.close()


def register_user(username: str, email: str, password: str = Field(min_length=8, max_length=64)) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashPassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cursor.execute(
    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
    (username, email, hashPassword),
)
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()