import tkinter as tk
from tkinter import messagebox
from presentation.main_window import open_main_window  # Import the main window function

# Hardcoded user credentials for validation (for now)
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"


def login():
    username = username_entry.get()
    password = password_entry.get()

    # Validate credentials
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        # Close the login window and open the main window
        login_window.destroy()  # Destroy the login window
        open_main_window()  # Open the main window
    else:
        messagebox.showerror("Login Error", "Invalid username or password")


def create_login_window():
    global login_window, username_entry, password_entry

    login_window = tk.Tk()
    login_window.title("Login - BITE AND BREW")

    # Cafe name label at the top
    cafe_name_label = tk.Label(login_window, text="BITE AND BREW", font=("Arial", 24))
    cafe_name_label.pack(pady=20)

    # Username label and entry
    username_label = tk.Label(login_window, text="Username:")
    username_label.pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    # Password label and entry
    password_label = tk.Label(login_window, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    # Login button
    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.pack(pady=20)

    # Start the Tkinter event loop for the login window
    login_window.mainloop()
