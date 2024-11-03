import sqlite3
import hashlib

# Connect to (or create) the database
connection = sqlite3.connect('users.db')
curs = connection.cursor()

# Create a users table if it doesn't exist
curs.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Insert a sample user (Replace with your own username/password)
username = ''
password = hash_password('')

curs.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', (username, password))

# Commit and close the connection
connection.commit()
connection.close()
