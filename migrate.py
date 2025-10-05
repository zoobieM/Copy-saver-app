import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "snippets.db")

print(f"Database path: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Check current columns
c.execute("PRAGMA table_info(snippets)")
columns = c.fetchall()
print("\nCurrent columns:")
for col in columns:
    print(f"  - {col[1]}")

existing_columns = [col[1] for col in columns]

# Add created_at if it doesn't exist
if 'created_at' not in existing_columns:
    try:
        c.execute("ALTER TABLE snippets ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        print("\n✓ Added created_at column")
    except Exception as e:
        print(f"\n✗ Error adding created_at: {e}")
else:
    print("\n- created_at column already exists")

# Add last_edited if it doesn't exist
if 'last_edited' not in existing_columns:
    try:
        c.execute("ALTER TABLE snippets ADD COLUMN last_edited TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        print("✓ Added last_edited column")
    except Exception as e:
        print(f"✗ Error adding last_edited: {e}")
else:
    print("- last_edited column already exists")

conn.commit()

# Verify the changes
c.execute("PRAGMA table_info(snippets)")
columns = c.fetchall()
print("\nUpdated columns:")
for col in columns:
    print(f"  - {col[1]}")

conn.close()
print("\n✓ Migration complete! Your snippets are safe.")
