import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'database', 'coffee_shop.db')

def create_inventory_item(item_name, quantity, price):
    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")
    if price <= 0:
        raise ValueError("Price must be a positive number.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if item_name already exists
    cursor.execute("SELECT * FROM inventory WHERE item_name = ?", (item_name,))
    if cursor.fetchone():
        raise ValueError("Item name already exists.")

    cursor.execute('''
        INSERT INTO inventory (item_name, quantity, price) VALUES (?, ?, ?)
    ''', (item_name, quantity, price))
    conn.commit()
    conn.close()

def get_inventory_item_by_id(item_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    return item

def update_inventory_item(item_id, item_name, quantity, price):
    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")
    if price <= 0:
        raise ValueError("Price must be a positive number.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if the new item_name already exists (and isn't the current item)
    cursor.execute("SELECT * FROM inventory WHERE item_name = ? AND id != ?", (item_name, item_id))
    if cursor.fetchone():
        raise ValueError("Item name already exists.")

    cursor.execute('''
        UPDATE inventory SET item_name = ?, quantity = ?, price = ? WHERE id = ?
    ''', (item_name, quantity, price, item_id))
    conn.commit()
    conn.close()

def delete_inventory_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
