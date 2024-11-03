import sys
from flask import Flask, render_template, request
from gpiozero import Button
from gpiozero import OutputDevice
import time

button = Button(18, pull_up=True)
garage_door = OutputDevice(4, active_high=True, initial_value=False)

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Replace with a secure secret key in production

# Replace with actual secure credentials
USERNAME = "admin"
PASSWORD = "password"


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
        if username == USERNAME and password == PASSWORD:
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


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/button/open', methods=['GET', 'POST'])
def garage_open():
    garage_door_remote.on()
    time.sleep(1)
    garage_door_remote.off()
    return "Garage is opening"


@app.route('/button/close', methods=['GET', 'POST'])
def garage_close():
    garage_door_remote.on()
    time.sleep(1)
    garage_door_remote.off()
    return "Garage is closing"


@app.route('/button/status', methods=['GET', 'POST'])
def garage_status():
    if button.is_pressed:
        return "Garage is closed"
    else:
        return "Garage is open"


@app.route('/button/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return "Server shutting down..."


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    finally:
        garage_door_remote.close()  # Clean up GPIO on exit
