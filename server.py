from flask import Flask, request, jsonify
from db import get_or_create_user, can_user_request, get_score, get_requests_today
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)

PORT = int(os.environ.get("PORT", 8000))
app.run(host="0.0.0.0", port=PORT)

@app.route('/api/check_user', methods=['POST'])
def check_user():
    data = request.get_json()
    user_id = data.get('user_id')
    username = data.get('username')

    if not user_id or not username:
        return jsonify({'error': 'Missing user_id or username'}), 400

    get_or_create_user(user_id, username)
    allowed = can_user_request(user_id)
    score = get_score(user_id)
    attempts = get_requests_today(user_id)

    return jsonify({
        'username': username,
        'points': score,
        'attempts_today': attempts,
        'limit_reached': not allowed
    })

if __name__ == '__main__':
    app.run(port=8000)
