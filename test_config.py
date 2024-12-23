from config import DB_PATH
import sqlite3
import os

def test_database_connection():
    """Test the connection to the database and display the database path."""
    # Print the resolved database path
    print(f"Database path from config: {DB_PATH}")

    # Check if the database file exists
    if not os.path.exists(DB_PATH):
        print("Warning: The database file does not exist. Ensure it is initialized.")
        return

    # Attempt to connect to the database
    try:
        with sqlite3.connect(DB_PATH) as conn:
            print("Connected to the database successfully.")
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_database_connection()
