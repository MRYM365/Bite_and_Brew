import sqlite3
from business_logic.expense_logic import update_expense, get_expense_by_id

# Helper function to add a test expense (for testing purposes)
def add_test_expense():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO expenses (expense_name, amount, date) VALUES (?, ?, ?)
    ''', ('Test Expense', 100.0, '2024-12-01'))
    conn.commit()
    conn.close()

# Test 1: Valid Update
def test_valid_update():
    # First, add a test expense
    add_test_expense()

    # Fetch the expense before update
    expense = get_expense_by_id(1)
    print(f"Before Update: {expense}")

    # Update the expense
    update_expense(1, 'Updated Expense', 200.75, '2024-12-16')

    # Fetch the expense after update
    updated_expense = get_expense_by_id(1)
    print(f"After Update: {updated_expense}")

# Test 2: Invalid Expense Name (Empty)
def test_invalid_expense_name():
    try:
        update_expense(1, '', 200.75, '2024-12-16')  # Empty expense name
    except ValueError as e:
        print(f"Error: {e}")

# Test 3: Invalid Amount (Negative)
def test_invalid_amount():
    try:
        update_expense(1, 'Updated Expense', -50.0, '2024-12-16')  # Negative amount
    except ValueError as e:
        print(f"Error: {e}")

# Test 4: Invalid Date Format
def test_invalid_date_format():
    try:
        update_expense(1, 'Updated Expense', 200.75, '2024/12/31')  # Invalid date format
    except ValueError as e:
        print(f"Error: {e}")

# Run the tests
test_valid_update()
test_invalid_expense_name()
test_invalid_amount()
test_invalid_date_format()
