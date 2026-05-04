import sqlite3
conn = sqlite3.connect("todo.db")
rows = conn.execute("SELECT id, title, priority, done, created_at FROM task").fetchall()
print(rows)
conn.close()