import os

# Get the base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Centralized database pat
DB_PATH = os.path.join(BASE_DIR, 'database', 'database' ,'coffee_shop.db')

# Ensure the database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Optional: Print the resolved path for debugging (comment this out in production)
print(f"Resolved Database Path: {DB_PATH}")
