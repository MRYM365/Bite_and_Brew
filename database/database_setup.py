import sqlite3
import os
from config import DB_PATH

# Ensure the directory for the database exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def initialize_database():
    """Initialize the SQLite database and create tables if they don't exist."""
    try:
        # Create a connection to the SQLite database
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # Create the tables
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('admin', 'staff'))
            )
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL UNIQUE,
                quantity INTEGER NOT NULL CHECK (quantity >= 0),
                price REAL NOT NULL CHECK (price > 0)
            )
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_name TEXT NOT NULL,
                amount REAL NOT NULL CHECK (amount > 0),
                date TEXT NOT NULL
            )
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_date TEXT NOT NULL,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                total_price REAL NOT NULL CHECK (total_price >= 0)
            )
            ''')

            print("Tables created successfully in the database!")
    except sqlite3.OperationalError as oe:
        print(f"Operational error: {oe}")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Initialize the database
if __name__ == "__main__":
    initialize_database()
