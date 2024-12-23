import sys
import os
from business_logic.user_logic import create_user, get_user_by_id, update_user, delete_user

# Add the project root to the system path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def test_users():
    print("Starting Users Table Tests...\n")

    try:
        # Step 1: Create a user
        print("Creating a user...")
        create_user("test_user", "test_pass", "staff")
        print("User created successfully.")

        # Step 2: Fetch the created user
        print("\nFetching the created user...")
        user = get_user_by_id(1)  # Replace '1' with a dynamic ID if possible
        print(f"Fetched user: {user}")

        # Step 3: Update the user
        print("\nUpdating the user...")
        update_user(1, "updated_user", "updated_pass", "admin")
        updated_user = get_user_by_id(1)
        print(f"Updated user: {updated_user}")

        # Step 4: Delete the user
        print("\nDeleting the user...")
        delete_user(1)
        deleted_user = get_user_by_id(1)
        print(f"User after deletion (should be None): {deleted_user}")

    except Exception as e:
        print(f"An error occurred during testing: {e}")
        return

    print("\nUsers Table Tests Completed Successfully.")


if __name__ == "__main__":
    test_users()
