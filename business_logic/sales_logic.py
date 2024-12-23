import sqlite3
from config import DB_PATH


def get_item_details(item_name):
    """Helper function to fetch item details from inventory."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, price, quantity FROM inventory WHERE item_name = ?", (item_name,))
        return cursor.fetchone()


def create_sale(sale_date, item_name, quantity):
    """Create a new sale and adjust inventory levels."""
    if not item_name or quantity <= 0:
        raise ValueError("Invalid input. Item name must be non-empty and quantity must be positive.")

    item = get_item_details(item_name)
    if not item:
        raise ValueError(f"Item '{item_name}' not found in inventory.")

    item_id, item_price, available_quantity = item
    if quantity > available_quantity:
        raise ValueError(f"Insufficient inventory for item '{item_name}' (available: {available_quantity}).")

    total_price = item_price * quantity

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Insert the sale
        cursor.execute('''
            INSERT INTO sales (sale_date, item_name, quantity, total_price) VALUES (?, ?, ?, ?)
        ''', (sale_date, item_name, quantity, total_price))

        # Update inventory
        cursor.execute('''
            UPDATE inventory SET quantity = quantity - ? WHERE id = ?
        ''', (quantity, item_id))
        conn.commit()

    print(f"Sale of '{item_name}' created successfully. Total Price: {total_price}")


def get_sale_by_id(sale_id):
    """Retrieve a sale by its ID."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM sales WHERE id = ?
        ''', (sale_id,))
        sale = cursor.fetchone()
        if sale:
            return sale
        else:
            print(f"No sale found with id {sale_id}.")
            return None


def update_sale(sale_id, sale_date, item_name, quantity):
    """Update an existing sale and adjust inventory levels."""
    if not item_name or quantity <= 0:
        raise ValueError("Invalid input. Item name must be non-empty and quantity must be positive.")

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Check if sale exists
        cursor.execute("SELECT * FROM sales WHERE id = ?", (sale_id,))
        existing_sale = cursor.fetchone()
        if not existing_sale:
            raise ValueError(f"No sale found with id {sale_id}.")

        old_quantity = existing_sale[3]  # Assuming quantity is the 4th column
        item = get_item_details(item_name)
        if not item:
            raise ValueError(f"Item '{item_name}' not found in inventory.")

        item_id, item_price, available_quantity = item
        new_quantity_difference = quantity - old_quantity

        if new_quantity_difference > available_quantity:
            raise ValueError(f"Insufficient inventory for item '{item_name}' (available: {available_quantity}).")

        total_price = item_price * quantity

        # Update the sale
        cursor.execute('''
            UPDATE sales SET sale_date = ?, item_name = ?, quantity = ?, total_price = ? WHERE id = ?
        ''', (sale_date, item_name, quantity, total_price, sale_id))

        # Adjust inventory levels
        cursor.execute('''
            UPDATE inventory SET quantity = quantity - ? WHERE id = ?
        ''', (new_quantity_difference, item_id))
        conn.commit()

    print(f"Sale with id {sale_id} updated successfully.")


def delete_sale(sale_id):
    """Delete a sale and adjust inventory levels."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Check if sale exists
        cursor.execute("SELECT * FROM sales WHERE id = ?", (sale_id,))
        sale = cursor.fetchone()
        if not sale:
            raise ValueError(f"No sale found with id {sale_id}.")

        item_name = sale[2]  # Assuming item_name is the 3rd column
        quantity = sale[3]  # Assuming quantity is the 4th column

        item = get_item_details(item_name)
        if not item:
            raise ValueError(f"Item '{item_name}' not found in inventory.")

        item_id = item[0]

        # Delete the sale
        cursor.execute("DELETE FROM sales WHERE id = ?", (sale_id,))

        # Restore inventory
        cursor.execute('''
            UPDATE inventory SET quantity = quantity + ? WHERE id = ?
        ''', (quantity, item_id))
        conn.commit()

    print(f"Sale with id {sale_id} deleted successfully and inventory restored.")
