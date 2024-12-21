import tkinter as tk

def open_users_window(main_window):
    # Create the users window
    users_window = tk.Toplevel(main_window)  # Create a new window on top of the main window
    users_window.title("Users Management - BITE AND BREW")

    # Cafe name at the top (optional, but keeps the design consistent)
    cafe_name_label = tk.Label(users_window, text="BITE AND BREW - Users Management", font=("Arial", 20))
    cafe_name_label.pack(pady=20)

    # Add content for the Users section
    label = tk.Label(users_window, text="Manage Users", font=("Helvetica", 16))
    label.pack(pady=20)

    # Example button to add a user
    add_user_button = tk.Button(users_window, text="Add User", command=open_add_user_window)
    add_user_button.pack(pady=10)

    # Back button to close the users window and return to the main window
    back_button = tk.Button(users_window, text="Back to Main", command=users_window.destroy)
    back_button.pack(pady=10)

    # Start the Tkinter main loop for the users window
    users_window.mainloop()

def open_add_user_window():
    # This function can be expanded later to open a new window for adding a user
    messagebox.showinfo("Add User", "This feature is not yet implemented.")
