import sys
import os

# Add the project root to the system path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from business_logic.user_logic import create_user, get_user_by_id, update_user, delete_user


def test_users():
    print("Testing Users Table...")

    # Create a user
    create_user("test_user", "test_pass", "staff")
    print("User created.")

    # Read the user
    user = get_user_by_id(1)  # Assuming this is the first user
    print(f"User fetched: {user}")

    # Update the user
    update_user(1, "updated_user", "updated_pass", "admin")
    updated_user = get_user_by_id(1)
    print(f"User after update: {updated_user}")

    # Delete the user
    delete_user(1)
    deleted_user = get_user_by_id(1)
    print(f"User after deletion: {deleted_user}")

if __name__ == "__main__":
    test_users()
