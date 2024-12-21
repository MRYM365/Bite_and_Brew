import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'database', 'coffee_shop.db')

def create_user(username, password, role):
    if role not in ['admin', 'staff']:
        raise ValueError("Role must be either 'admin' or 'staff'.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        raise ValueError("Username already exists.")

    cursor.execute('''
        INSERT INTO users (username, password, role) VALUES (?, ?, ?)
    ''', (username, password, role))
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user(user_id, username, password, role):
    if role not in ['admin', 'staff']:
        raise ValueError("Role must be either 'admin' or 'staff'.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if the new username already exists (and isn't the current user)
    cursor.execute("SELECT * FROM users WHERE username = ? AND id != ?", (username, user_id))
    if cursor.fetchone():
        raise ValueError("Username already exists.")

    cursor.execute('''
        UPDATE users SET username = ?, password = ?, role = ? WHERE id = ?
    ''', (username, password, role, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
