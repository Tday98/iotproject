import hashlib
import os
import secrets
import signal
import sqlite3
import time
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session
from gpiozero import Button
from gpiozero import OutputDevice

button = Button(18, pull_up=True)
garage_door = OutputDevice(4, active_high=True, initial_value=False)

PID = os.getpid()
app = Flask(__name__)
app.secret_key = secrets.token_bytes(16)  # Replace with a secure secret key in production

DATABASE = 'users.db'
username = ""


def get_db_connection():
    '''
    Simple SQLite database connection
    :return:
    '''
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Login required decorator
def login_required(f):
    '''
    looked up a simple way to run a session connection
     with Flask and found this simple code.
    :param f:
    :return:
    '''

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login function that retrieves username and password from forum that it generates from the return of itself
    :return:
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = hash_password(password)

        # connection to attach the database
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed))
            user = cursor.fetchone()
            connection.close()
        except sqlite3.Error:
            return render_template('login.html', error_message="Invalid database request, please try again.")

        if user:
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            return render_template('login.html', error_message="Invalid login, please try again.")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))


@app.route('/')
@login_required
def home():
    garage_door_status = not button.is_pressed

    return render_template('home.html', username=username, garage_door_status=garage_door_status)


@app.route('/button/open', methods=['GET', 'POST'])
@login_required
def garage_open():
    '''
    Flips the relay I have hooked to my soldered garage remote to trigger the
    RF signal to send to the garage to open/close it.
    :return:
    '''
    garage_door.on()
    time.sleep(1)
    garage_door.off()
    return "Garage is opening"


@app.route('/button/close', methods=['GET', 'POST'])
@login_required
def garage_close():
    '''
    Flips the relay I have hooked to my soldered garage remote to trigger the
    RF signal to send to the garage to open/close it.
    :return:
    '''
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
    '''
    Mimics a SIGINT command from the terminal which terminates the webapp
    also frees the GPIO pins.
    '''
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
