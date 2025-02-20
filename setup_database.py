import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('attendance.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table for storing student information
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    face_encoding BLOB NOT NULL
)
''')

# Create a table for storing attendance records
cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    name TEXT NOT NULL,           
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    emotion TEXT NOT NULL           
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database setup complete.")