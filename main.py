import os
import sqlite3
import hashlib
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

DATABASE = 'app.db'

def connect_db():
    return sqlite3.connect(DATABASE)

# Vulnerable login function with SQL Injection
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = connect_db()
    cursor = conn.cursor()
    # Vulnerable SQL query (SQL Injection)
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    user = cursor.fetchone()

    if user:
        return "Logged in successfully!"
    else:
        return "Invalid credentials"

# Vulnerable file upload function with Insecure Deserialization
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(f"/tmp/{file.filename}")
    return "File uploaded successfully"

# Vulnerable command execution with Command Injection
@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host')
    # Command injection vulnerability
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True)
    return result.stdout

# Vulnerable method exposing sensitive data
@app.route('/debug', methods=['GET'])
def debug():
    # Exposing sensitive environment variables
    debug_info = os.environ
    return str(debug_info)

# Weak password hashing method
def hash_password(password):
    # Using MD5, which is weak and vulnerable to collisions
    return hashlib.md5(password.encode()).hexdigest()

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    hashed_password = hash_password(password)

    conn = connect_db()
    cursor = conn.cursor()
    # Vulnerable to SQL Injection
    cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{hashed_password}')")
    conn.commit()

    return "User registered successfully!"

# Vulnerable dynamic template rendering
@app.route('/profile', methods=['GET'])
def profile():
    username = request.args.get('username')
    # Vulnerable to Server-Side Template Injection (SSTI)
    template = f"<h1>Welcome {username}</h1>"
    return render_template_string(template)

if __name__ == "__main__":
    app.run(debug=True)
