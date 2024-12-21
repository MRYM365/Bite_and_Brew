import tkinter as tk
from tkinter import messagebox


def open_expenses_window():
    # Create a new Tkinter window for the Expenses section
    expenses_window = tk.Toplevel()  # Use Toplevel to create a new window, keeping the main window intact
    expenses_window.title("Expenses - BITE AND BREW")

    # Set the window size
    expenses_window.geometry("600x400")

    # Add a label to indicate the section
    label = tk.Label(expenses_window, text="This is the Expenses section", font=("Helvetica", 16))
    label.pack(pady=20)

    # Add a button to close the expenses window
    close_button = tk.Button(expenses_window, text="Close", command=expenses_window.destroy)
    close_button.pack(pady=10)

    # Start the Tkinter event loop for this window
    expenses_window.mainloop()
