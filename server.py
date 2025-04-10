from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import db  # импорт твоего db.py

app = Flask(__name__)
CORS(app)

@app.route("/api/check_user", methods=["POST"])
def check_user():
    data = request.get_json()
    user_id = data.get("user_id")
    username = data.get("username")

    db.get_or_create_user(user_id, username)
    can_request = db.can_user_request(user_id)
    score = db.get_score(user_id)

    response = {
        "username": username,
        "points": score,
        "attempts_today": db.get_requests_today(user_id := int(user_id)),
        "limit_reached": not can_request
    }

    return jsonify(response)

# Добавим метод в db.py, если его нет:
# def get_requests_today(user_id):
#     cursor.execute("SELECT requests_today FROM users WHERE id = ?", (user_id,))
#     result = cursor.fetchone()
#     return result[0] if result else 0

# Для запуска сервера:
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
