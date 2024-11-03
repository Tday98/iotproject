import sys
from flask import Flask, render_template, request
from gpiozero import Button
from gpiozero import OutputDevice
import time

button = Button(18, pull_up=True)
garage_door = OutputDevice(4, active_high=True, initial_value=False)

app = Flask(__name__)


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


@app.route('/shutdown', methods=['POST'])
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
