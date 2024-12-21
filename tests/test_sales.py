import sys
import os

# Add the root project directory to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from business_logic.sales_logic import create_sale, get_sale_by_id, update_sale, delete_sale

def test_sales():
    print("Testing Sales Table...")

    # Create a sale
    create_sale("2024-12-15", "Test Item", 2, 19.98)
    print("Sale created.")

    # Read the sale
    sale = get_sale_by_id(1)
    print(f"Sale fetched: {sale}")

    # Update the sale
    update_sale(1, "2024-12-16", "Updated Item", 3, 29.97)
    updated_sale = get_sale_by_id(1)
    print(f"Sale after update: {updated_sale}")

    # Delete the sale
    delete_sale(1)
    deleted_sale = get_sale_by_id(1)
    print(f"Sale after deletion: {deleted_sale}")

if __name__ == "__main__":
    test_sales()
