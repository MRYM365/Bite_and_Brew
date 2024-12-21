import tkinter as tk
from presentation.users_window import open_users_window  # Import Users window function
from presentation.inventory_window import open_inventory_window  # Import Inventory window function
from presentation.expenses_window import open_expenses_window  # Import Expenses window function
from presentation.sales_window import open_sales_window  # Import Sales window function


def open_main_window():
    main_window = tk.Tk()
    main_window.title("BITE AND BREW - Main Window")

    # Cafe name at the top
    cafe_name_label = tk.Label(main_window, text="BITE AND BREW", font=("Arial", 24))
    cafe_name_label.pack(pady=20)

    # Add a navigation panel or buttons for the main window
    # For example, buttons for Users, Inventory, Sales, etc.

    users_button = tk.Button(main_window, text="Users", command=lambda: open_users_window(main_window))
    users_button.pack(pady=10)

    inventory_button = tk.Button(main_window, text="Inventory", command=lambda: open_inventory_window(main_window))
    inventory_button.pack(pady=10)

    expenses_button = tk.Button(main_window, text="Expenses", command=lambda: open_expenses_window(main_window))
    expenses_button.pack(pady=10)

    sales_button = tk.Button(main_window, text="Sales", command=lambda: open_sales_window(main_window))
    sales_button.pack(pady=10)

    # Start the Tkinter main loop for the main window
    main_window.mainloop()
