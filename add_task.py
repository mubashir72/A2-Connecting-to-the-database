import sqlite3

DB_NAME = "tasks.db"

title = input("Enter task title: ")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO tasks (title, done) VALUES (?, ?)",
    (title, False)
)

conn.commit()

print(f"Task added successfully with ID {cursor.lastrowid}")

conn.close()