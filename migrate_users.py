import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "snippets.db")

print("Adding user authentication to database...")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create users table
try:
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Users table created")
except Exception as e:
    print(f"Error creating users table: {e}")

# Add user_id column to snippets if it doesn't exist
try:
    c.execute("ALTER TABLE snippets ADD COLUMN user_id INTEGER")
    print("✓ Added user_id column to snippets")
except:
    print("- user_id column already exists or error occurred")

# Create a default user for existing snippets
default_username = input("\nEnter a username for your existing snippets (e.g., 'admin'): ").strip()
default_password = input("Enter a password (min 6 characters): ").strip()

if len(default_password) < 6:
    print("❌ Password too short. Using 'password123' as default.")
    default_password = "password123"

password_hash = generate_password_hash(default_password)

try:
    c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (default_username, password_hash))
    user_id = c.lastrowid
    print(f"✓ Created user: {default_username}")
    
    # Assign all existing snippets to this user
    c.execute("UPDATE snippets SET user_id = ? WHERE user_id IS NULL", (user_id,))
    updated = c.rowcount
    print(f"✓ Assigned {updated} existing snippets to {default_username}")
except Exception as e:
    print(f"Error: {e}")

conn.commit()
conn.close()

print("\n🎉 Migration complete!")
print(f"You can now login with username: {default_username}")
