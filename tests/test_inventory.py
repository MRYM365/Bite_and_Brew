import sys
import os

# Add the root project directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from business_logic.inventory_logic import create_inventory_item, get_inventory_item_by_id, update_inventory_item, delete_inventory_item

def test_inventory():
    print("Testing Inventory Table...")

    # Create an inventory item
    create_inventory_item("Test Item", 10, 5.99)
    print("Inventory item created.")

    # Read the inventory item
    item = get_inventory_item_by_id(1)
    print(f"Inventory item fetched: {item}")

    # Update the inventory item
    update_inventory_item(1, "Updated Item", 20, 9.99)
    updated_item = get_inventory_item_by_id(1)
    print(f"Inventory item after update: {updated_item}")

    # Delete the inventory item
    delete_inventory_item(1)
    deleted_item = get_inventory_item_by_id(1)
    print(f"Inventory item after deletion: {deleted_item}")

if __name__ == "__main__":
    test_inventory()
