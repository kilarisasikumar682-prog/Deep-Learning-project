from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# In-memory storage for users
users = {}

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if username in users:
        return jsonify({'message': 'User already exists.'}), 400

    # Hash the password
    hashed_password = generate_password_hash(password, method='sha256')
    users[username] = hashed_password
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username not in users:
        return jsonify({'message': 'User does not exist.'}), 404

    if check_password_hash(users[username], password):
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Invalid password.'}), 401

if __name__ == '__main__':
    app.run(debug=True)