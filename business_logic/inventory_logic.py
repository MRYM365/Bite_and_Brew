import sqlite3
from config import DB_PATH


def validate_inputs(item_name, quantity, price):
    """Helper function to validate inputs."""
    if not item_name or len(item_name.strip()) == 0 or len(item_name) > 100:
        raise ValueError("Item name must not be empty, should not exceed 100 characters, and should not consist only of whitespace.")
    if not isinstance(quantity, int) or quantity < 0:
        raise ValueError("Quantity must be a non-negative integer.")
    if not isinstance(price, (int, float)) or price <= 0:
        raise ValueError("Price must be a positive number.")


def check_item_exists(cursor, item_id):
    """Helper function to check if an item exists by ID."""
    cursor.execute("SELECT id FROM inventory WHERE id = ?", (item_id,))
    return cursor.fetchone() is not None


def create_inventory_item(item_name, quantity, price):
    """Create a new inventory item."""
    validate_inputs(item_name, quantity, price)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # Check if item_name already exists
            cursor.execute("SELECT id FROM inventory WHERE item_name = ?", (item_name,))
            if cursor.fetchone():
                raise ValueError("Item name already exists.")

            cursor.execute('''
                INSERT INTO inventory (item_name, quantity, price) VALUES (?, ?, ?)
            ''', (item_name, quantity, price))
            conn.commit()
            print(f"Item '{item_name}' added successfully.")
    except sqlite3.Error as e:
        print(f"Database error while creating item: {e}")


def get_inventory_item_by_id(item_id):
    """Retrieve an inventory item by its ID."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, item_name, quantity, price FROM inventory WHERE id = ?", (item_id,))
            item = cursor.fetchone()
            if item:
                return item
            else:
                print(f"No inventory item found with id {item_id}.")
                return None
    except sqlite3.Error as e:
        print(f"Database error while fetching item: {e}")
        return None


def update_inventory_item(item_id, item_name, quantity, price):
    """Update an existing inventory item."""
    validate_inputs(item_name, quantity, price)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # Check if the new item_name already exists (and isn't the current item)
            cursor.execute("SELECT id FROM inventory WHERE item_name = ? AND id != ?", (item_name, item_id))
            if cursor.fetchone():
                raise ValueError("Item name already exists.")

            # Ensure the item_id exists
            if not check_item_exists(cursor, item_id):
                raise ValueError(f"No inventory item found with id {item_id}.")

            cursor.execute('''
                UPDATE inventory SET item_name = ?, quantity = ?, price = ? WHERE id = ?
            ''', (item_name, quantity, price, item_id))
            conn.commit()
            print(f"Item with id {item_id} updated successfully.")
    except sqlite3.Error as e:
        print(f"Database error while updating item: {e}")


def delete_inventory_item(item_id):
    """Delete an inventory item by its ID."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # Ensure the item_id exists
            if not check_item_exists(cursor, item_id):
                raise ValueError(f"No inventory item found with id {item_id}.")

            cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
            conn.commit()
            print(f"Item with id {item_id} deleted successfully.")
    except sqlite3.Error as e:
        print(f"Database error while deleting item: {e}")
