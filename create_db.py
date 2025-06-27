# create_db.py

import sqlite3

# Connect (this will create the file if not exist)
conn = sqlite3.connect('database/users.db')
cursor = conn.cursor()

# Create the 'users' table with required fields
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        dob TEXT NOT NULL,
        gender TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

print("Database created successfully with 'users' table!")
