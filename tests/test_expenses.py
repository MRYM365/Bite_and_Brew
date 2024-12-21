import sys
import os

# Add the root project directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from business_logic.expense_logic import create_expense, get_expense_by_id, update_expense, delete_expense

def test_expenses():
    print("Testing Expenses Table...")

    # Create an expense
    create_expense("Test Expense", 100.50, "2024-12-15")
    print("Expense created.")

    # Read the expense
    expense = get_expense_by_id(1)
    print(f"Expense fetched: {expense}")

    # Update the expense
    update_expense(1, "Updated Expense", 200.75, "2024-12-16")
    updated_expense = get_expense_by_id(1)
    print(f"Expense after update: {updated_expense}")

    # Delete the expense
    delete_expense(1)
    deleted_expense = get_expense_by_id(1)
    print(f"Expense after deletion: {deleted_expense}")

if __name__ == "__main__":
    test_expenses()
