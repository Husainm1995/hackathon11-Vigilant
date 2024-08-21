import sqlite3
import bcrypt

def register_user(username, password):
    conn = sqlite3.connect('secure_app.db')
    cursor = conn.cursor()
    
    # Hash the password securely with bcrypt
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Use parameterized queries to prevent SQL injection
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

    print("User registered securely!")

# Example usage
register_user('new_user', 'secure_password')
