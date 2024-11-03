import sys

from flask import Flask, render_template, request
from gpiozero import Button
from gpiozero import OutputDevice
import time

button = Button(18, pull_up=True)
garage_door = OutputDevice(4, active_high=True, initial_value=False)

app = Flask(__name__)


def garage_toggle():
    garage_door.on()
    time.sleep(1)
    garage_door.off()

def garage_value():
    if button.is_pressed():
        return "Garage is closed"
    else:
        return "Garage is open"

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/button/<action>', methods=['GET', 'POST'])
def button_action(action):
    if request.method == 'POST':
        if action == 'open':
            garage_toggle()
            return "Garage door opening!"
        elif action == 'close':
            garage_toggle()
            return "Garage door closing!"
        elif action == 'status':
            return garage_value()
        elif action == 'kill':
            return sys.exit()
    return "Something went wrong."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
