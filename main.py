from flask import Flask, jsonify
from flask_caching import Cache
import redis

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:5000/1'})
db = redis.Redis(host='redis', port=5000, db=1, decode_responses=True)


@app.route('/match/<int:user_id>')
@cache.cached(timeout=0)
def get_match(user_id):
    users = get_users()
    requested_user = get_user(user_id, users)
    if not requested_user:
        return jsonify([])

    potential_matches = []
    for user in users:
        if user['id'] != user_id:
            common_hobbies = set(user['hobbies']) & set(requested_user['hobbies'])
            potential_matches.append({
                'id': user['id'],
                'name': user['name'],
                'hobbies': list(common_hobbies)
            })

    potential_matches = sorted(potential_matches, key=lambda m: len(m['hobbies']), reverse=True)
    return jsonify(potential_matches)


def get_users():
    return [
        {
            "id": 1,
            "name": "Meet",
            "hobbies": ["Music", "Chess", "Drawing"]
        },
        {
            "id": 2,
            "name": "Pari Singh",
            "hobbies": ["Music", "Cooking", "Reading"]
        },
        {
            "id": 3,
            "name": "Naina Patel",
            "hobbies": ["Music", "Chess", "Dance"]
        },
        {
            "id": 4,
            "name": "Amy Bhatt",
            "hobbies": ["Cooking"]
        }
    ]


def get_user(user_id, users):
    for user in users:
        if user['id'] == user_id:
            return user
    return None


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
