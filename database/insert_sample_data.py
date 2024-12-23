import sqlite3
import bcrypt  # Ensure bcrypt is installed for password hashing
from config import DB_PATH


def hash_password(password):
    """Helper function to hash passwords."""
    try:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return hashed
    except Exception as e:
        print(f"Error hashing password: {e}")
        raise


def insert_sample_data():
    """Insert sample data into the database."""
    try:
        # Create a connection to the SQLite database
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # Insert sample data into the 'users' table
            admin_password = hash_password('admin123')
            staff_password = hash_password('password123')

            print(f"Hashed admin password: {admin_password}")
            print(f"Hashed staff password: {staff_password}")

            cursor.executemany('''
            INSERT OR IGNORE INTO users (username, password, role) VALUES
            (?, ?, ?)
            ''', [
                ('admin', admin_password, 'admin'),
                ('john_doe', staff_password, 'staff'),
            ])

            # Insert sample data into the 'inventory' table
            inventory_data = [
                ('Coffee', 50, 2.5),
                ('Tea', 30, 1.8),
                ('Pastry', 20, 3.0),
            ]
            cursor.executemany('''
            INSERT OR IGNORE INTO inventory (item_name, quantity, price) VALUES
            (?, ?, ?)
            ''', inventory_data)

            # Insert sample data into the 'expenses' table
            expenses_data = [
                ('Rent', 500.0, '2024-12-01'),
                ('Utilities', 100.0, '2024-12-05'),
            ]
            cursor.executemany('''
            INSERT OR IGNORE INTO expenses (expense_name, amount, date) VALUES
            (?, ?, ?)
            ''', expenses_data)

            # Insert sample data into the 'sales' table
            sales_data = [
                ('2024-12-10', 'Coffee', 3, 7.5),
                ('2024-12-10', 'Pastry', 2, 6.0),
            ]
            cursor.executemany('''
            INSERT OR IGNORE INTO sales (sale_date, item_name, quantity, total_price) VALUES
            (?, ?, ?, ?)
            ''', sales_data)

            print("Sample data inserted successfully into the database!")

    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e}")
    except sqlite3.OperationalError as e:
        print(f"Operational Error: {e}")
    except sqlite3.Error as e:
        print(f"An SQLite error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Run the function
if __name__ == "__main__":
    insert_sample_data()
