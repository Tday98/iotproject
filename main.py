import os
import sys
from flask import Flask, render_template, request, redirect, url_for, session
from gpiozero import Button
from gpiozero import OutputDevice
from functools import wraps
import sqlite3
import hashlib
import time

button = Button(18, pull_up=True)
garage_door = OutputDevice(4, active_high=True, initial_value=False)

PID = os.getpid()
app = Flask(__name__)
app.secret_key = "super_secret_key"  # Replace with a secure secret key in production

DATABASE = 'users.db'


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = hash_password(password)

        connection = get_db_connection()
        user = connection.execute("SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, hashed)).fetchone()
        connection.close()

        if user:
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            return "Invalid credentials, please try again."
    return '''
        <form method="post">
            <label>Username: <input type="text" name="username"></label>
            <label>Password: <input type="password" name="password"></label>
            <button type="submit">Login</button>
        </form>
    '''


@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))


@app.route('/')
@login_required
def home():
    return render_template('home.html')


@app.route('/button/open', methods=['GET', 'POST'])
@login_required
def garage_open():
    garage_door.on()
    time.sleep(1)
    garage_door.off()
    return "Garage is opening"


@app.route('/button/close', methods=['GET', 'POST'])
@login_required
def garage_close():
    garage_door.on()
    time.sleep(1)
    garage_door.off()
    return "Garage is closing"


@app.route('/button/status', methods=['GET', 'POST'])
@login_required
def garage_status():
    if button.is_pressed:
        return "Garage is closed"
    else:
        return "Garage is open"


@app.route('/button/shutdown', methods=['POST'])
@login_required
def shutdown():
    shutdown_server()
    return "Server shutting down..."


def shutdown_server():
    garage_door.close()
    button.close()
    pid = os.getpid()
    assert pid == PID
    os.kill(pid, signal.SIGINT)
    return "OK", 200


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    finally:
        garage_door.close()  # Clean up GPIO on exit
