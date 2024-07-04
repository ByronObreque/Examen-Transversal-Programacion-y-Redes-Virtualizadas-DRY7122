import pyotp    # Generates one-time passwords
import sqlite3  # Database for username/passwords
import hashlib  # Secure hashes and message digests
import uuid     # For creating universally unique identifiers
from flask import Flask, request, jsonify

app = Flask(__name__)

db_name = 'test.db'

@app.route('/')
def index():
    return '¡Bienvenido al sistema de gestión de usuarios y contraseñas!'

@app.route('/signup/v1', methods=['POST'])
def signup_v1():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH
           (USERNAME  TEXT    PRIMARY KEY NOT NULL,
            PASSWORD  TEXT    NOT NULL);''')
    conn.commit()
    username = request.form['username']
    password = request.form['password']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute("INSERT INTO USER_HASH (USERNAME,PASSWORD) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        return "El nombre de usuario ya ha sido registrado."
    print('username: ', username, ' hashed_password: ', hashed_password)
    return "Registro exitoso"

def verify_hash(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "SELECT PASSWORD FROM USER_HASH WHERE USERNAME = ?"
    c.execute(query, (username,))
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == hashlib.sha256(password.encode()).hexdigest()

@app.route('/login/v1', methods=['GET', 'POST'])
def login_v1():
    error = None
    if request.method == 'POST':
        if verify_hash(request.form['username'], request.form['password']):
            error = 'Inicio de sesión exitoso'
        else:
            error = 'Usuario o contraseña inválidos'
    else:
        error = 'Método inválido'
    return error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800, ssl_context='adhoc')

