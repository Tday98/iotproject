from flask import Flask, render_template, request
from gpiozero import Button
from gpiozero import OutputDevice

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/button/<action>', methods=['GET', 'POST'])
def button_action(action):
    if request.method == 'POST':
        if action == 'open':
            return "Garage door opening!"
        elif action == 'close':
            return "Garage door closing!"
        elif action == 'kill':
            return ""
        elif action == 'kill':
            return "Shutting Down"
    return "Something went wrong."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)