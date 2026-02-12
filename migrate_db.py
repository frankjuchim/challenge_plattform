import sqlite3
import os

# Path to the database
# Based on config.py: os.path.join(BASE_DIR, "data", "challenge.db")
# Current directory is BASE_DIR for the app usually.
db_path = os.path.join("data", "challenge.db")

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

print(f"Migrating database at {db_path}...")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if column exists
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [info[1] for info in cursor.fetchall()]
    
    if "allowed_extension" in columns:
        print("Column 'allowed_extension' already exists.")
    else:
        print("Adding column 'allowed_extension'...")
        # Add the column with a default value of .pde
        cursor.execute("ALTER TABLE tasks ADD COLUMN allowed_extension VARCHAR(10) DEFAULT '.pde'")
        conn.commit()
        print("Migration successful.")
        
except Exception as e:
    print(f"Error during migration: {e}")
    conn.rollback()
finally:
    conn.close()
