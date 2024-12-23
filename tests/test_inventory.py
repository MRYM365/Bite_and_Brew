import sys
import os
from business_logic.inventory_logic import create_inventory_item, get_inventory_item_by_id, update_inventory_item, delete_inventory_item

# Add the root project directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_inventory():
    print("Starting Inventory Table Tests...\n")

    try:
        # Step 1: Create an inventory item
        print("Creating inventory item...")
        create_inventory_item("Test Item", 10, 5.99)
        print("Inventory item created successfully.")

        # Step 2: Retrieve the created item
        print("\nFetching created inventory item...")
        item = get_inventory_item_by_id(1)  # Replace '1' with a dynamic ID if possible
        print(f"Fetched inventory item: {item}")

        # Step 3: Update the inventory item
        print("\nUpdating inventory item...")
        update_inventory_item(1, "Updated Item", 20, 9.99)
        updated_item = get_inventory_item_by_id(1)
        print(f"Updated inventory item: {updated_item}")

        # Step 4: Delete the inventory item
        print("\nDeleting inventory item...")
        delete_inventory_item(1)
        deleted_item = get_inventory_item_by_id(1)
        print(f"Inventory item after deletion (should be None): {deleted_item}")

    except Exception as e:
        print(f"An error occurred during testing: {e}")
        return

    print("\nInventory Table Tests Completed Successfully.")


if __name__ == "__main__":
    test_inventory()
