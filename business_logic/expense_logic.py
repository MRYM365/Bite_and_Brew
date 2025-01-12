import sqlite3
from config import DB_PATH


def create_expense(expense_name, amount, date):
    """Add a new expense to the database."""
    if not expense_name or amount <= 0:
        raise ValueError("Invalid expense data. Name cannot be empty, and amount must be positive.")
    if not validate_date_format(date):
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO expenses (expense_name, amount, date) VALUES (?, ?, ?)",
                (expense_name, amount, date),
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error while creating expense: {e}")
        raise


def get_expense_by_id(expense_id):
    """Retrieve an expense by its ID."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error while fetching expense: {e}")
        raise


def update_expense(expense_id, expense_name, amount, date):
    """Update an existing expense."""
    if not expense_name or amount <= 0:
        raise ValueError("Invalid expense data. Name cannot be empty, and amount must be positive.")
    if not validate_date_format(date):
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE expenses SET expense_name = ?, amount = ?, date = ? WHERE id = ?",
                (expense_name, amount, date, expense_id),
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error while updating expense: {e}")
        raise


def delete_expense(expense_id):
    """Delete an expense by its ID."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error while deleting expense: {e}")
        raise


def validate_date_format(date):
    """Validate the date format as YYYY-MM-DD."""
    try:
        from datetime import datetime
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False
