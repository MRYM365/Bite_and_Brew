import tkinter as tk
from tkinter import messagebox
import sqlite3
from config import DB_PATH
import bcrypt  # To securely hash and verify passwords

# --- Utility Functions ---
def validate_credentials(username, password):
    """Validate credentials against the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # Retrieve hashed password for the given username
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                hashed_password = result[0]
                # Use bcrypt to compare the provided password with the stored hashed password
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    return True
            return False
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return False

# --- Content Management ---
def clear_content(content_frame):
    """Clear all widgets in the content frame."""
    for widget in content_frame.winfo_children():
        widget.destroy()

# --- Users Section ---
def display_users(content_frame):
    """Display the Users Management section."""
    clear_content(content_frame)

    section_title = tk.Label(content_frame, text="Users Management", font=("Arial", 20, "bold"))
    section_title.pack(pady=10)

    table_frame = tk.Frame(content_frame)
    table_frame.pack(pady=10)

    headers = ["ID", "Username", "Role", "Actions"]
    for col, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=15).grid(row=0, column=col)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, role FROM users")
            users = cursor.fetchall()

            for row, user in enumerate(users, start=1):
                user_id, username, role = user
                tk.Label(table_frame, text=user_id, font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=0)
                tk.Label(table_frame, text=username, font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=1)
                tk.Label(table_frame, text=role, font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=2)

                # Edit and Delete Buttons
                tk.Button(table_frame, text="Edit", font=("Arial", 10), bg="orange", fg="black",
                          command=lambda uid=user_id: open_edit_user_form(content_frame, uid)).grid(row=row, column=3)
                tk.Button(table_frame, text="Delete", font=("Arial", 10), bg="red", fg="white",
                          command=lambda uid=user_id: delete_user(content_frame, uid)).grid(row=row, column=4)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    tk.Button(content_frame, text="Add User", command=lambda: open_add_user_form(content_frame),
              font=("Arial", 12), bg="blue", fg="white").pack(pady=10)

def open_add_user_form(content_frame):
    """Open a form to add a new user."""
    clear_content(content_frame)

    tk.Label(content_frame, text="Add New User", font=("Arial", 20, "bold")).pack(pady=10)

    username_label = tk.Label(content_frame, text="Username:")
    username_label.pack(pady=5)
    username_entry = tk.Entry(content_frame)
    username_entry.pack(pady=5)

    password_label = tk.Label(content_frame, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(content_frame, show="*")
    password_entry.pack(pady=5)

    role_label = tk.Label(content_frame, text="Role (admin/staff):")
    role_label.pack(pady=5)
    role_entry = tk.Entry(content_frame)
    role_entry.pack(pady=5)

    def save_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        role = role_entry.get().strip()

        if not username or not password or not role:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        if role not in ["admin", "staff"]:
            messagebox.showerror("Input Error", "Role must be 'admin' or 'staff'.")
            return

        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                               (username, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), role))
                conn.commit()
                messagebox.showinfo("Success", "User added successfully.")
                display_users(content_frame)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    tk.Button(content_frame, text="Save", command=save_user, bg="green", fg="white").pack(pady=20)

def open_edit_user_form(content_frame, user_id):
    """Open a form to edit an existing user."""
    clear_content(content_frame)

    tk.Label(content_frame, text="Edit User", font=("Arial", 20, "bold")).pack(pady=10)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, role FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            messagebox.showerror("Error", "User not found.")
            display_users(content_frame)
            return

        username, role = user

    username_label = tk.Label(content_frame, text="Username:")
    username_label.pack(pady=5)
    username_entry = tk.Entry(content_frame)
    username_entry.insert(0, username)
    username_entry.pack(pady=5)

    role_label = tk.Label(content_frame, text="Role (admin/staff):")
    role_label.pack(pady=5)
    role_entry = tk.Entry(content_frame)
    role_entry.insert(0, role)
    role_entry.pack(pady=5)

    def save_changes():
        new_username = username_entry.get().strip()
        new_role = role_entry.get().strip()

        if not new_username or not new_role:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        if new_role not in ["admin", "staff"]:
            messagebox.showerror("Input Error", "Role must be 'admin' or 'staff'.")
            return

        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET username = ?, role = ? WHERE id = ?", (new_username, new_role, user_id))
                conn.commit()
                messagebox.showinfo("Success", "User updated successfully.")
                display_users(content_frame)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    tk.Button(content_frame, text="Save Changes", command=save_changes, bg="green", fg="white").pack(pady=20)

def delete_user(content_frame, user_id):
    """Delete a user from the database."""
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?"):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                messagebox.showinfo("Success", "User deleted successfully.")
                display_users(content_frame)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

# Similar CRUD functions for Inventory, Expenses, and Sales can be added following this pattern.

# --- Utility Functions ---
def clear_content(content_frame):
    """Clear all widgets in the content frame."""
    for widget in content_frame.winfo_children():
        widget.destroy()

def execute_query(query, params=()):
    """Execute a query and return the results."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return []

# --- CRUD for Inventory ---
def display_inventory(content_frame):
    """Display the Inventory Management section."""
    clear_content(content_frame)

    section_title = tk.Label(content_frame, text="Inventory Management", font=("Arial", 20, "bold"))
    section_title.pack(pady=10)

    # Table for Inventory
    table_frame = tk.Frame(content_frame)
    table_frame.pack(pady=10)

    headers = ["ID", "Item Name", "Quantity", "Price", "Actions"]
    for col, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=15).grid(row=0, column=col)

    # Fetch and display inventory
    items = execute_query("SELECT id, item_name, quantity, price FROM inventory")
    for row, item in enumerate(items, start=1):
        item_id, item_name, quantity, price = item

        tk.Label(table_frame, text=item_id, font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=0)
        tk.Label(table_frame, text=item_name, font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=1)
        tk.Label(table_frame, text=quantity, font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=2)
        tk.Label(table_frame, text=f"${price:.2f}", font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=3)

        # Edit Button
        tk.Button(table_frame, text="Edit", font=("Arial", 10), bg="orange", fg="black",
                  command=lambda i_id=item_id: open_edit_inventory_form(content_frame, i_id)).grid(row=row, column=4)

        # Delete Button
        tk.Button(table_frame, text="Delete", font=("Arial", 10), bg="red", fg="white",
                  command=lambda i_id=item_id: delete_inventory_item(content_frame, i_id)).grid(row=row, column=5)

    # Add Item Button
    tk.Button(content_frame, text="Add Item", command=lambda: open_add_inventory_form(content_frame),
              font=("Arial", 12), bg="blue", fg="white").pack(pady=10)

def open_add_inventory_form(content_frame):
    """Open a form to add a new inventory item."""
    clear_content(content_frame)
    tk.Label(content_frame, text="Add New Item", font=("Arial", 20, "bold")).pack(pady=10)

    # Form Fields
    tk.Label(content_frame, text="Item Name:").pack(pady=5)
    item_name_entry = tk.Entry(content_frame)
    item_name_entry.pack(pady=5)

    tk.Label(content_frame, text="Quantity:").pack(pady=5)
    quantity_entry = tk.Entry(content_frame)
    quantity_entry.pack(pady=5)

    tk.Label(content_frame, text="Price:").pack(pady=5)
    price_entry = tk.Entry(content_frame)
    price_entry.pack(pady=5)

    def save_item():
        item_name = item_name_entry.get().strip()
        try:
            quantity = int(quantity_entry.get().strip())
            price = float(price_entry.get().strip())
            if not item_name or quantity < 0 or price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Invalid input. Please provide valid values.")
            return

        execute_query("INSERT INTO inventory (item_name, quantity, price) VALUES (?, ?, ?)", (item_name, quantity, price))
        messagebox.showinfo("Success", "Item added successfully!")
        display_inventory(content_frame)

    tk.Button(content_frame, text="Save", command=save_item, bg="green", fg="white").pack(pady=20)

def open_edit_inventory_form(content_frame, item_id):
    """Open a form to edit an inventory item."""
    clear_content(content_frame)

    # Fetch item details
    item = execute_query("SELECT item_name, quantity, price FROM inventory WHERE id = ?", (item_id,))
    if not item:
        messagebox.showerror("Error", "Item not found.")
        display_inventory(content_frame)
        return

    item_name, quantity, price = item[0]

    tk.Label(content_frame, text="Edit Item", font=("Arial", 20, "bold")).pack(pady=10)

    # Form Fields
    tk.Label(content_frame, text="Item Name:").pack(pady=5)
    item_name_entry = tk.Entry(content_frame)
    item_name_entry.insert(0, item_name)
    item_name_entry.pack(pady=5)

    tk.Label(content_frame, text="Quantity:").pack(pady=5)
    quantity_entry = tk.Entry(content_frame)
    quantity_entry.insert(0, quantity)
    quantity_entry.pack(pady=5)

    tk.Label(content_frame, text="Price:").pack(pady=5)
    price_entry = tk.Entry(content_frame)
    price_entry.insert(0, price)
    price_entry.pack(pady=5)

    def save_changes():
        try:
            new_item_name = item_name_entry.get().strip()
            new_quantity = int(quantity_entry.get().strip())
            new_price = float(price_entry.get().strip())
            if not new_item_name or new_quantity < 0 or new_price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Invalid input. Please provide valid values.")
            return

        execute_query("UPDATE inventory SET item_name = ?, quantity = ?, price = ? WHERE id = ?",
                      (new_item_name, new_quantity, new_price, item_id))
        messagebox.showinfo("Success", "Item updated successfully!")
        display_inventory(content_frame)

    tk.Button(content_frame, text="Save Changes", command=save_changes, bg="green", fg="white").pack(pady=20)

def delete_inventory_item(content_frame, item_id):
    """Delete an inventory item."""
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
        execute_query("DELETE FROM inventory WHERE id = ?", (item_id,))
        messagebox.showinfo("Success", "Item deleted successfully!")
        display_inventory(content_frame)

def display_expenses(content_frame):
    """Display the Expenses Management section."""
    clear_content(content_frame)

    section_title = tk.Label(content_frame, text="Expenses Management", font=("Arial", 20, "bold"))
    section_title.pack(pady=10)

    # Table for Expenses
    table_frame = tk.Frame(content_frame)
    table_frame.pack(pady=10)

    headers = ["ID", "Expense Name", "Amount", "Date", "Actions"]
    for col, header in enumerate(headers):
        header_label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=15)
        header_label.grid(row=0, column=col)

    # Fetch and display expenses
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, expense_name, amount, date FROM expenses")
            expenses = cursor.fetchall()

            for row, expense in enumerate(expenses, start=1):
                expense_id, name, amount, date = expense

                # Display expense data
                tk.Label(table_frame, text=expense_id, font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=0)
                tk.Label(table_frame, text=name, font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=1)
                tk.Label(table_frame, text=f"${amount:.2f}", font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=2)
                tk.Label(table_frame, text=date, font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=3)

                # Edit Button
                edit_button = tk.Button(table_frame, text="Edit", font=("Arial", 10), bg="orange", fg="black",
                                        command=lambda eid=expense_id: open_edit_expense_form(content_frame, eid))
                edit_button.grid(row=row, column=4)

                # Delete Button
                delete_button = tk.Button(table_frame, text="Delete", font=("Arial", 10), bg="red", fg="white",
                                          command=lambda eid=expense_id: delete_expense(content_frame, eid))
                delete_button.grid(row=row, column=5)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    # Add Expense Button
    add_expense_button = tk.Button(content_frame, text="Add Expense", command=lambda: open_add_expense_form(content_frame), font=("Arial", 12), bg="blue", fg="white")
    add_expense_button.pack(pady=10)


def open_add_expense_form(content_frame):
    """Open a form to add a new expense."""
    clear_content(content_frame)

    tk.Label(content_frame, text="Add New Expense", font=("Arial", 20, "bold")).pack(pady=10)

    expense_name_label = tk.Label(content_frame, text="Expense Name:")
    expense_name_label.pack(pady=5)
    expense_name_entry = tk.Entry(content_frame)
    expense_name_entry.pack(pady=5)

    amount_label = tk.Label(content_frame, text="Amount:")
    amount_label.pack(pady=5)
    amount_entry = tk.Entry(content_frame)
    amount_entry.pack(pady=5)

    date_label = tk.Label(content_frame, text="Date (YYYY-MM-DD):")
    date_label.pack(pady=5)
    date_entry = tk.Entry(content_frame)
    date_entry.pack(pady=5)

    def save_expense():
        name = expense_name_entry.get().strip()
        amount = amount_entry.get().strip()
        date = date_entry.get().strip()

        if not name or not amount or not date:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a positive number.")
            return

        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO expenses (expense_name, amount, date) VALUES (?, ?, ?)", (name, amount, date))
                conn.commit()
                messagebox.showinfo("Success", "Expense added successfully.")
                display_expenses(content_frame)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    tk.Button(content_frame, text="Save Expense", command=save_expense, font=("Arial", 12), bg="green", fg="white").pack(pady=20)


def open_edit_expense_form(content_frame, expense_id):
    """Open a form to edit an existing expense."""
    clear_content(content_frame)

    tk.Label(content_frame, text="Edit Expense", font=("Arial", 20, "bold")).pack(pady=10)

    # Fetch expense details
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT expense_name, amount, date FROM expenses WHERE id = ?", (expense_id,))
        expense = cursor.fetchone()
        if not expense:
            messagebox.showerror("Error", "Expense not found.")
            display_expenses(content_frame)
            return

        name, amount, date = expense

    expense_name_label = tk.Label(content_frame, text="Expense Name:")
    expense_name_label.pack(pady=5)
    expense_name_entry = tk.Entry(content_frame)
    expense_name_entry.insert(0, name)
    expense_name_entry.pack(pady=5)

    amount_label = tk.Label(content_frame, text="Amount:")
    amount_label.pack(pady=5)
    amount_entry = tk.Entry(content_frame)
    amount_entry.insert(0, f"{amount:.2f}")
    amount_entry.pack(pady=5)

    date_label = tk.Label(content_frame, text="Date (YYYY-MM-DD):")
    date_label.pack(pady=5)
    date_entry = tk.Entry(content_frame)
    date_entry.insert(0, date)
    date_entry.pack(pady=5)

    def save_changes():
        new_name = expense_name_entry.get().strip()
        new_amount = amount_entry.get().strip()
        new_date = date_entry.get().strip()

        if not new_name or not new_amount or not new_date:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        try:
            new_amount = float(new_amount)
            if new_amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a positive number.")
            return

        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE expenses SET expense_name = ?, amount = ?, date = ? WHERE id = ?", (new_name, new_amount, new_date, expense_id))
                conn.commit()
                messagebox.showinfo("Success", "Expense updated successfully.")
                display_expenses(content_frame)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    tk.Button(content_frame, text="Save Changes", command=save_changes, font=("Arial", 12), bg="green", fg="white").pack(pady=20)


def delete_expense(content_frame, expense_id):
    """Delete an expense from the database."""
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this expense?"):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
                conn.commit()
                messagebox.showinfo("Success", "Expense deleted successfully.")
                display_expenses(content_frame)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")


def display_sales(content_frame):
    """Display the Sales Management section."""
    clear_content(content_frame)

    section_title = tk.Label(content_frame, text="Sales Management", font=("Arial", 20, "bold"))
    section_title.pack(pady=10)

    # Table for Sales
    table_frame = tk.Frame(content_frame)
    table_frame.pack(pady=10)

    headers = ["ID", "Sale Date", "Item Name", "Quantity", "Total Price", "Actions"]
    for col, header in enumerate(headers):
        header_label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=15)
        header_label.grid(row=0, column=col)

    # Fetch and display sales
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, sale_date, item_name, quantity, total_price FROM sales")
            sales = cursor.fetchall()

            for row, sale in enumerate(sales, start=1):
                sale_id, sale_date, item_name, quantity, total_price = sale

                # Display sale data
                tk.Label(table_frame, text=sale_id, font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=0)
                tk.Label(table_frame, text=sale_date, font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=1)
                tk.Label(table_frame, text=item_name, font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=2)
                tk.Label(table_frame, text=quantity, font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=3)
                tk.Label(table_frame, text=f"${total_price:.2f}", font=("Arial", 10), borderwidth=1, relief="solid", width=15).grid(row=row, column=4)

                # Edit Button
                edit_button = tk.Button(table_frame, text="Edit", font=("Arial", 10), bg="orange", fg="black",
                                        command=lambda sid=sale_id: open_edit_sale_form(content_frame, sid))
                edit_button.grid(row=row, column=5)

                # Delete Button
                delete_button = tk.Button(table_frame, text="Delete", font=("Arial", 10), bg="red", fg="white",
                                          command=lambda sid=sale_id: delete_sale(content_frame, sid))
                delete_button.grid(row=row, column=6)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    # Add Sale Button
    add_sale_button = tk.Button(content_frame, text="Add Sale", command=lambda: open_add_sale_form(content_frame), font=("Arial", 12), bg="blue", fg="white")
    add_sale_button.pack(pady=10)


def open_add_sale_form(content_frame):
    """Open a form to add a new sale."""
    clear_content(content_frame)

    tk.Label(content_frame, text="Add New Sale", font=("Arial", 20, "bold")).pack(pady=10)

    sale_date_label = tk.Label(content_frame, text="Sale Date (YYYY-MM-DD):")
    sale_date_label.pack(pady=5)
    sale_date_entry = tk.Entry(content_frame)
    sale_date_entry.pack(pady=5)

    item_name_label = tk.Label(content_frame, text="Item Name:")
    item_name_label.pack(pady=5)
    item_name_entry = tk.Entry(content_frame)
    item_name_entry.pack(pady=5)

    quantity_label = tk.Label(content_frame, text="Quantity:")
    quantity_label.pack(pady=5)
    quantity_entry = tk.Entry(content_frame)
    quantity_entry.pack(pady=5)

    def save_sale():
        sale_date = sale_date_entry.get().strip()
        item_name = item_name_entry.get().strip()
        quantity = quantity_entry.get().strip()

        if not sale_date or not item_name or not quantity:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Quantity must be a positive integer.")
            return

        try:
            # Calculate total price based on inventory
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT price FROM inventory WHERE item_name = ?", (item_name,))
                result = cursor.fetchone()
                if not result:
                    messagebox.showerror("Input Error", f"Item '{item_name}' not found in inventory.")
                    return

                item_price = result[0]
                total_price = item_price * quantity

                # Insert into sales table
                cursor.execute("INSERT INTO sales (sale_date, item_name, quantity, total_price) VALUES (?, ?, ?, ?)",
                               (sale_date, item_name, quantity, total_price))

                # Update inventory quantity
                cursor.execute("UPDATE inventory SET quantity = quantity - ? WHERE item_name = ?", (quantity, item_name))
                conn.commit()

                messagebox.showinfo("Success", "Sale added successfully.")
                display_sales(content_frame)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    tk.Button(content_frame, text="Save Sale", command=save_sale, font=("Arial", 12), bg="green", fg="white").pack(pady=20)


def open_edit_sale_form(content_frame, sale_id):
    """Open a form to edit an existing sale."""
    clear_content(content_frame)

    tk.Label(content_frame, text="Edit Sale", font=("Arial", 20, "bold")).pack(pady=10)

    # Fetch sale details
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sale_date, item_name, quantity FROM sales WHERE id = ?", (sale_id,))
        sale = cursor.fetchone()
        if not sale:
            messagebox.showerror("Error", "Sale not found.")
            display_sales(content_frame)
            return

        sale_date, item_name, quantity = sale

    sale_date_label = tk.Label(content_frame, text="Sale Date (YYYY-MM-DD):")
    sale_date_label.pack(pady=5)
    sale_date_entry = tk.Entry(content_frame)
    sale_date_entry.insert(0, sale_date)
    sale_date_entry.pack(pady=5)

    item_name_label = tk.Label(content_frame, text="Item Name:")
    item_name_label.pack(pady=5)
    item_name_entry = tk.Entry(content_frame)
    item_name_entry.insert(0, item_name)
    item_name_entry.pack(pady=5)

    quantity_label = tk.Label(content_frame, text="Quantity:")
    quantity_label.pack(pady=5)
    quantity_entry = tk.Entry(content_frame)
    quantity_entry.insert(0, quantity)
    quantity_entry.pack(pady=5)

    def save_changes():
        new_sale_date = sale_date_entry.get().strip()
        new_item_name = item_name_entry.get().strip()
        new_quantity = quantity_entry.get().strip()

        if not new_sale_date or not new_item_name or not new_quantity:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        try:
            new_quantity = int(new_quantity)
            if new_quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Quantity must be a positive integer.")
            return

        try:
            # Update sale details
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE sales SET sale_date = ?, item_name = ?, quantity = ? WHERE id = ?",
                               (new_sale_date, new_item_name, new_quantity, sale_id))
                conn.commit()
                messagebox.showinfo("Success", "Sale updated successfully.")
                display_sales(content_frame)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    tk.Button(content_frame, text="Save Changes", command=save_changes, font=("Arial", 12), bg="green", fg="white").pack(pady=20)


def delete_sale(content_frame, sale_id):
    """Delete a sale from the database."""
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this sale?"):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
                conn.commit()
                messagebox.showinfo("Success", "Sale deleted successfully.")
                display_sales(content_frame)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")




def open_main_window():
    """Create and display the main application window."""
    main_window = tk.Tk()
    main_window.title("BITE AND BREW")
    main_window.geometry("800x600")

    nav_panel = tk.Frame(main_window, width=200, bg="#333333")
    nav_panel.pack(side=tk.LEFT, fill=tk.Y)

    content_frame = tk.Frame(main_window, bg="#f7f7f7")
    content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    nav_buttons = [
        ("Users", lambda: display_users(content_frame)),
        ("Inventory", lambda: display_inventory(content_frame)),
        ("Expenses", lambda: display_expenses(content_frame)),
        ("Sales", lambda: display_sales(content_frame)),
    ]

    nav_buttons = [
        ("Users", lambda: display_users(content_frame)),
        ("Inventory", lambda: display_inventory(content_frame)),
        ("Expenses", lambda: display_expenses(content_frame)),
        ("Sales", lambda: display_sales(content_frame)),
    ]

    nav_buttons = [
        ("Users", lambda: display_users(content_frame)),
        ("Inventory", lambda: display_inventory(content_frame)),
        ("Expenses", lambda: display_expenses(content_frame)),
        ("Sales", lambda: display_sales(content_frame)),
    ]

    for text, command in nav_buttons:
        tk.Button(nav_panel, text=text, command=command, font=("Arial", 14), bg="#555555", fg="white", width=20, height=2).pack(pady=10)

    display_users(content_frame)  # Default section
    main_window.mainloop()

def create_login_window():
    """Create and display the login window."""
    login_window = tk.Tk()
    login_window.title("Login - BITE AND BREW")
    login_window.geometry("400x300")

    username_label = tk.Label(login_window, text="Username:", font=("Arial", 12))
    username_label.pack(pady=5)
    username_entry = tk.Entry(login_window, font=("Arial", 12))
    username_entry.pack(pady=5)

    password_label = tk.Label(login_window, text="Password:", font=("Arial", 12))
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Input Error", "Both username and password are required.")
            return

        if validate_credentials(username, password):
            messagebox.showinfo("Login Success", "Welcome to BITE AND BREW!")
            login_window.destroy()
            open_main_window()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    tk.Button(login_window, text="Login", command=login, font=("Arial", 12), bg="green", fg="white").pack(pady=20)
    login_window.mainloop()

if __name__ == "__main__":
    create_login_window()
