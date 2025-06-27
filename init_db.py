import sqlite3

# Connect to your database (it will create if not exists)
conn = sqlite3.connect('database/users.db')
cursor = conn.cursor()

# Create the 'users' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Insert a demo user (optional)
cursor.execute('''
INSERT OR IGNORE INTO users (username, password)
VALUES (?, ?)
''', ('admin', 'admin123'))  # You can change username/password

# Commit changes and close connection
conn.commit()
conn.close()

print("Database initialized successfully ")
