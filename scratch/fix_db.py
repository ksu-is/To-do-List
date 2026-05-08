import sqlite3
import os

db_path = 'instance/todo.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check current columns
    cursor.execute("PRAGMA table_info(task)")
    columns = [column[1] for column in cursor.fetchall()]
    
    print(f"Current columns: {columns}")
    
    if 'priority' not in columns:
        print("Adding 'priority' column...")
        cursor.execute("ALTER TABLE task ADD COLUMN priority VARCHAR(50) DEFAULT 'Medium'")
        
    if 'category' not in columns:
        print("Adding 'category' column...")
        cursor.execute("ALTER TABLE task ADD COLUMN category VARCHAR(50) DEFAULT 'List 1'")
        
    conn.commit()
    conn.close()
    print("Database updated successfully.")
else:
    print("Database file not found. It will be created by Flask.")
