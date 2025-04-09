import sqlite3
from datetime import datetime

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    score INTEGER DEFAULT 100,
    request_date TEXT,
    request_count INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()
