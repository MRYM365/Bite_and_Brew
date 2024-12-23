import sys
import os
from business_logic.sales_logic import create_sale, get_sale_by_id, update_sale, delete_sale

# Add the root project directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_sales():
    print("Starting Sales Table Tests...\n")

    try:
        # Step 1: Create a sale
        print("Creating sale...")
        create_sale("2024-12-15", "Test Item", 2, 19.98)
        print("Sale created successfully.")

        # Step 2: Retrieve the created sale
        print("\nFetching created sale...")
        sale = get_sale_by_id(1)  # Replace '1' with a dynamic ID if possible
        print(f"Fetched sale: {sale}")

        # Step 3: Update the sale
        print("\nUpdating sale...")
        update_sale(1, "2024-12-16", "Updated Item", 3, 29.97)
        updated_sale = get_sale_by_id(1)
        print(f"Updated sale: {updated_sale}")

        # Step 4: Delete the sale
        print("\nDeleting sale...")
        delete_sale(1)
        deleted_sale = get_sale_by_id(1)
        print(f"Sale after deletion (should be None): {deleted_sale}")

    except Exception as e:
        print(f"An error occurred during testing: {e}")
        return

    print("\nSales Table Tests Completed Successfully.")


if __name__ == "__main__":
    test_sales()
