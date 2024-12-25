import tkinter as tk
from tkinter import messagebox, Label, Entry, Button
from main import open_main_window  # Import the main window function directly
import sqlite3
from config import DB_PATH
import bcrypt  # To securely hash and verify passwords


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


def create_login_window():
    """Create and display the login window."""
    login_window = tk.Tk()
    login_window.title("Login - BITE AND BREW")
    login_window.geometry("400x300")

    # Username and password entries
    username_label = tk.Label(login_window, text="Username:", font=("Arial", 12))
    username_label.pack(pady=5)
    username_entry = tk.Entry(login_window, font=("Arial", 12))
    username_entry.pack(pady=5)

    password_label = tk.Label(login_window, text="Password:", font=("Arial", 12))
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
    password_entry.pack(pady=5)

    def login():
        """Handle the login process."""
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Input Error", "Both username and password are required.")
            return

        if validate_credentials(username, password):
            try:
                with sqlite3.connect(DB_PATH) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
                    result = cursor.fetchone()
                    if result:
                        user_role = result[0]  # Get the user's role
                        print(f"DEBUG: User Role = {user_role}")  # Debug print
                        messagebox.showinfo("Login Success", f"Welcome, {username} ({user_role.capitalize()})!")
                        login_window.destroy()
                        open_main_window(user_role)  # Pass `user_role` to the main window
                    else:
                        messagebox.showerror("Login Error", "Role not found for the user.")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

    # Login button
    tk.Button(login_window, text="Login", command=login, font=("Arial", 12), bg="green", fg="white").pack(pady=20)
    login_window.mainloop()






if __name__ == "__main__":
    create_login_window()
