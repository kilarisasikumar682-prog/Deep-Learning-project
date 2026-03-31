from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample user data (in a real application, use a database)
users = {"user@example.com": "password"}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email in users and users[email] == password:
        return jsonify({'message': 'Login successful!'}), 200
    return jsonify({'message': 'Invalid credentials!'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Add user registration logic here, e.g., store in database
    users[email] = password
    return jsonify({'message': 'User registered successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True)