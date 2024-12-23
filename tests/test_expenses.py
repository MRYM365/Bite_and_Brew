import sys
import os
from business_logic.expense_logic import create_expense, get_expense_by_id, update_expense, delete_expense

# Add the root project directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_expenses():
    print("Starting Expenses Table Tests...\n")

    # Step 1: Create an expense
    print("Creating expense...")
    try:
        create_expense("Test Expense", 100.50, "2024-12-15")
        print("Expense created successfully.")
    except Exception as e:
        print(f"Error during expense creation: {e}")
        return

    # Step 2: Retrieve the created expense
    print("\nFetching created expense...")
    try:
        expense = get_expense_by_id(1)  # Replace '1' with a dynamic ID if possible
        print(f"Fetched expense: {expense}")
    except Exception as e:
        print(f"Error during expense retrieval: {e}")
        return

    # Step 3: Update the expense
    print("\nUpdating expense...")
    try:
        update_expense(1, "Updated Expense", 200.75, "2024-12-16")
        updated_expense = get_expense_by_id(1)
        print(f"Updated expense: {updated_expense}")
    except Exception as e:
        print(f"Error during expense update: {e}")
        return

    # Step 4: Delete the expense
    print("\nDeleting expense...")
    try:
        delete_expense(1)
        deleted_expense = get_expense_by_id(1)
        print(f"Expense after deletion (should be None): {deleted_expense}")
    except Exception as e:
        print(f"Error during expense deletion: {e}")
        return

    print("\nExpenses Table Tests Completed Successfully.")


if __name__ == "__main__":
    test_expenses()
