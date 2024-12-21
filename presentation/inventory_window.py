import tkinter as tk
from tkinter import messagebox


def open_inventory_window():
    # Create a new Tkinter window for the Inventory section
    inventory_window = tk.Toplevel()  # Use Toplevel to create a new window, keeping the main window intact
    inventory_window.title("Inventory - BITE AND BREW")

    # Set the window size
    inventory_window.geometry("600x400")

    # Add a label to indicate the section
    label = tk.Label(inventory_window, text="This is the Inventory section", font=("Helvetica", 16))
    label.pack(pady=20)

    # Add a button to close the inventory window
    close_button = tk.Button(inventory_window, text="Close", command=inventory_window.destroy)
    close_button.pack(pady=10)

    # Start the Tkinter event loop for this window
    inventory_window.mainloop()
