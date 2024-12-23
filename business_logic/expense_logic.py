import sqlite3
from config import DB_PATH  # Ensure DB_PATH is imported from your config
from business_logic.expense_logic import update_expense, get_expense_by_id


def add_test_expense():
    """Add a test expense and return its ID."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO expenses (expense_name, amount, date) VALUES (?, ?, ?)
            ''', ('Test Expense', 100.0, '2024-12-01'))
            conn.commit()
            return cursor.lastrowid  # Return the ID of the inserted expense
    except sqlite3.Error as e:
        print(f"Database error while adding test expense: {e}")
        return None


def test_valid_update():
    """Test updating an expense with valid data."""
    print("\nRunning Test 1: Valid Update")
    expense_id = add_test_expense()
    if not expense_id:
        print("Failed to add test expense.")
        return

    # Fetch the expense before the update
    expense = get_expense_by_id(expense_id)
    print(f"Before Update: {expense}")

    # Update the expense
    update_expense(expense_id, 'Updated Expense', 200.75, '2024-12-16')

    # Fetch the expense after the update
    updated_expense = get_expense_by_id(expense_id)
    print(f"After Update: {updated_expense}")


def test_invalid_expense_name():
    """Test updating an expense with an invalid (empty) name."""
    print("\nRunning Test 2: Invalid Expense Name")
    expense_id = add_test_expense()
    if not expense_id:
        print("Failed to add test expense.")
        return

    try:
        update_expense(expense_id, '', 200.75, '2024-12-16')  # Empty expense name
    except ValueError as e:
        print(f"Expected Error: {e}")


def test_invalid_amount():
    """Test updating an expense with a negative amount."""
    print("\nRunning Test 3: Invalid Amount")
    expense_id = add_test_expense()
    if not expense_id:
        print("Failed to add test expense.")
        return

    try:
        update_expense(expense_id, 'Updated Expense', -50.0, '2024-12-16')  # Negative amount
    except ValueError as e:
        print(f"Expected Error: {e}")


def test_invalid_date_format():
    """Test updating an expense with an invalid date format."""
    print("\nRunning Test 4: Invalid Date Format")
    expense_id = add_test_expense()
    if not expense_id:
        print("Failed to add test expense.")
        return

    try:
        update_expense(expense_id, 'Updated Expense', 200.75, '2024/12/31')  # Invalid date format
    except ValueError as e:
        print(f"Expected Error: {e}")


if __name__ == "__main__":
    test_valid_update()
    test_invalid_expense_name()
    test_invalid_amount()
    test_invalid_date_format()
