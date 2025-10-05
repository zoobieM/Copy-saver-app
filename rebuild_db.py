import sqlite3
import os
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "snippets.db")
BACKUP_PATH = os.path.join(BASE_DIR, f"snippets_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")

print(f"Database path: {DB_PATH}")

# Create backup
shutil.copy2(DB_PATH, BACKUP_PATH)
print(f"✓ Backup created: {BACKUP_PATH}")

# Connect to database
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Get all existing snippets
c.execute("SELECT id, content, tag FROM snippets")
old_snippets = c.fetchall()
print(f"\n✓ Found {len(old_snippets)} existing snippets")

# Drop old table
c.execute("DROP TABLE snippets")
print("✓ Dropped old table")

# Create new table with timestamp columns
c.execute("""
    CREATE TABLE snippets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        tag TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_edited TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
print("✓ Created new table with timestamp columns")

# Insert old snippets back
for snippet_id, content, tag in old_snippets:
    c.execute(
        "INSERT INTO snippets (id, content, tag) VALUES (?, ?, ?)",
        (snippet_id, content, tag)
    )

conn.commit()
print(f"✓ Restored all {len(old_snippets)} snippets")

# Verify
c.execute("PRAGMA table_info(snippets)")
columns = c.fetchall()
print("\n✓ New table structure:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

c.execute("SELECT COUNT(*) FROM snippets")
count = c.fetchone()[0]
print(f"\n✓ Total snippets in database: {count}")

conn.close()
print("\n🎉 Migration complete! All your snippets are safe with timestamps added!")
print(f"📦 Backup saved at: {BACKUP_PATH}")
