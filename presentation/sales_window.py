import tkinter as tk
from tkinter import messagebox

def open_sales_window(main_window):
    # Create the sales window
    sales_window = tk.Toplevel(main_window)  # Create a new window on top of the main window
    sales_window.title("Sales - BITE AND BREW")

    # Cafe name at the top (optional, but keeps the design consistent)
    cafe_name_label = tk.Label(sales_window, text="BITE AND BREW - Sales", font=("Arial", 20))
    cafe_name_label.pack(pady=20)

    # Add content for the Sales section
    label = tk.Label(sales_window, text="This is the Sales section", font=("Helvetica", 16))
    label.pack(pady=20)

    # Back button to close the sales window and return to the main window
    back_button = tk.Button(sales_window, text="Back to Main", command=sales_window.destroy)
    back_button.pack(pady=10)

    # Start the Tkinter main loop for the sales window
    sales_window.mainloop()
