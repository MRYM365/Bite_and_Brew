import sqlite3
import bcrypt  # Ensure bcrypt library is installed
from config import DB_PATH


def hash_password(password):
    """Hash a password using bcrypt."""
    try:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Error hashing password: {e}")


def check_password(password, hashed_password):
    """Verify a password against its hashed version."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        raise ValueError(f"Error checking password: {e}")



def validate_user_input(username, password, role):
    """Validate input for creating or updating a user."""
    if not username or len(username) > 50:
        raise ValueError("Username must not be empty and should be under 50 characters.")
    if not password or len(password) < 6:
        raise ValueError("Password must be at least 6 characters long.")
    if role not in ['admin', 'staff']:
        raise ValueError("Role must be 'admin' or 'staff'.")

def hash_password(password):
    """Hash a password securely."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_user(username, password, role):
    """Create a new user after validating input."""
    # Validate input
    validate_user_input(username, password, role)

    hashed_password = hash_password(password)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            raise ValueError("Username already exists.")

        # Insert the new user
        cursor.execute('''
            INSERT INTO users (username, password, role) VALUES (?, ?, ?)
        ''', (username, hashed_password, role))
        conn.commit()



def get_user_by_id(user_id):
    """Retrieve a user by their ID."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            if user:
                return user
            else:
                print(f"No user found with id {user_id}.")
                return None
    except sqlite3.Error as e:
        print(f"Database error while fetching user: {e}")
        return None


def update_user(user_id, username, password, role):
    """Update an existing user's information."""
    if not username or not password:
        raise ValueError("Username and password cannot be empty.")
    if role not in ['admin', 'staff']:
        raise ValueError("Role must be either 'admin' or 'staff'.")

    hashed_password = hash_password(password)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # Check if the user exists
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if not cursor.fetchone():
                raise ValueError(f"No user found with id {user_id}.")

            # Check if the new username already exists (and isn't the current user)
            cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (username, user_id))
            if cursor.fetchone():
                raise ValueError("Username already exists.")

            cursor.execute('''
                UPDATE users SET username = ?, password = ?, role = ? WHERE id = ?
            ''', (username, hashed_password, role, user_id))
            conn.commit()
        print(f"User with id {user_id} updated successfully.")
    except sqlite3.Error as e:
        print(f"Database error while updating user: {e}")


def delete_user(user_id):
    """Delete a user by their ID."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # Check if the user exists
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if not cursor.fetchone():
                raise ValueError(f"No user found with id {user_id}.")

            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
        print(f"User with id {user_id} deleted successfully.")
    except sqlite3.Error as e:
        print(f"Database error while deleting user: {e}")
