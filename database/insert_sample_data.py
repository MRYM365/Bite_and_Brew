import sqlite3
import os

# Define the path to the database
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'coffee_shop.db')

# Create a connection to the SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Insert sample data into the 'users' table
cursor.execute('''
INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'admin'),
('john_doe', 'password123', 'staff')
''')

# Insert sample data into the 'inventory' table
cursor.execute('''
INSERT INTO inventory (item_name, quantity, price) VALUES
('Coffee', 50, 2.5),
('Tea', 30, 1.8),
('Pastry', 20, 3.0)
''')

# Insert sample data into the 'expenses' table
cursor.execute('''
INSERT INTO expenses (expense_name, amount, date) VALUES
('Rent', 500.0, '2024-12-01'),
('Utilities', 100.0, '2024-12-05')
''')

# Insert sample data into the 'sales' table
cursor.execute('''
INSERT INTO sales (sale_date, item_name, quantity, total_price) VALUES
('2024-12-10', 'Coffee', 3, 7.5),
('2024-12-10', 'Pastry', 2, 6.0)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Sample data inserted successfully into the database!")
