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
    username_label = Label(login_window, text="Username:", font=("Arial", 12))
    username_label.pack(pady=5)
    username_entry = Entry(login_window, font=("Arial", 12))
    username_entry.pack(pady=5)

    password_label = Label(login_window, text="Password:", font=("Arial", 12))
    password_label.pack(pady=5)
    password_entry = Entry(login_window, show="*", font=("Arial", 12))
    password_entry.pack(pady=5)

    def login():
        """Handle the login process."""
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        # Validate inputs
        if not username or not password:
            messagebox.showerror("Input Error", "Both username and password are required.")
            return

        # Validate credentials
        if validate_credentials(username, password):
            messagebox.showinfo("Login Success", "Welcome to BITE AND BREW!")
            login_window.destroy()  # Close the login window
            open_main_window()  # Open the main window
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    # Login button
    login_button = Button(login_window, text="Login", command=login, font=("Arial", 12), bg="green", fg="white")
    login_button.pack(pady=20)

    # Start the Tkinter event loop for the login window
    login_window.mainloop()


if __name__ == "__main__":
    create_login_window()
