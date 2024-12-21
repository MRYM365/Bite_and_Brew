import sqlite3
import os

# Define the database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'database', 'coffee_shop.db')


# Create Sale
def create_sale(sale_date, item_name, quantity):
    if quantity <= 0:
        raise ValueError("Quantity must be a positive integer.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if the item exists in the inventory
    cursor.execute("SELECT * FROM inventory WHERE item_name = ?", (item_name,))
    item = cursor.fetchone()
    if not item:
        raise ValueError(f"Item '{item_name}' not found in inventory.")

    # Get the price of the item from the inventory
    item_price = item[3]  # The price is at index 3 (0-based index)

    # Calculate total price
    total_price = item_price * quantity

    # Insert the sale into the sales table
    cursor.execute('''
    INSERT INTO sales (sale_date, item_name, quantity, total_price) VALUES (?, ?, ?, ?)
    ''', (sale_date, item_name, quantity, total_price))
    conn.commit()
    conn.close()


# Read Sale
def get_sale_by_id(sale_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM sales WHERE id = ?
    ''', (sale_id,))
    sale = cursor.fetchone()
    conn.close()
    return sale


# Update Sale
def update_sale(sale_id, sale_date, item_name, quantity):
    if quantity <= 0:
        raise ValueError("Quantity must be a positive integer.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if the item exists in the inventory
    cursor.execute("SELECT * FROM inventory WHERE item_name = ?", (item_name,))
    item = cursor.fetchone()
    if not item:
        raise ValueError(f"Item '{item_name}' not found in inventory.")

    # Get the price of the item from the inventory
    item_price = item[3]  # The price is at index 3 (0-based index)

    # Calculate total price
    total_price = item_price * quantity

    # Update the sale in the sales table
    cursor.execute('''
    UPDATE sales SET sale_date = ?, item_name = ?, quantity = ?, total_price = ? WHERE id = ?
    ''', (sale_date, item_name, quantity, total_price, sale_id))
    conn.commit()
    conn.close()


# Delete Sale
def delete_sale(sale_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM sales WHERE id = ?
    ''', (sale_id,))
    conn.commit()
    conn.close()
