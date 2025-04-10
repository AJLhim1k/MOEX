import sqlite3
from datetime import datetime

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

def get_or_create_user(user_id, username):
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users (id, username, score, requests_today, last_request_date) VALUES (?, ?, 100, 0, ?)",
                       (user_id, username, datetime.now().date().isoformat()))
        conn.commit()

def can_user_request(user_id):
    today = datetime.now().date().isoformat()
    cursor.execute("SELECT requests_today, last_request_date FROM users WHERE id = ?", (user_id,))
    data = cursor.fetchone()
    if not data:
        return True
    requests_today, last_date = data
    if last_date != today:
        cursor.execute("UPDATE users SET requests_today = 1, last_request_date = ? WHERE id = ?", (today, user_id))
        conn.commit()
        return True
    elif requests_today < 5:
        cursor.execute("UPDATE users SET requests_today = requests_today + 1 WHERE id = ?", (user_id,))
        conn.commit()
        return True
    else:
        return False

def update_score(user_id, delta):
    cursor.execute("UPDATE users SET score = score + ? WHERE id = ?", (delta, user_id))
    conn.commit()

def get_score(user_id):
    cursor.execute("SELECT score FROM users WHERE id = ?", (user_id,))
    score = cursor.fetchone()
    return score[0] if score else None

def get_requests_today(user_id):
    cursor.execute("SELECT requests_today FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0
