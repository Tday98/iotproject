from gpiozero import Button
from gpiozero import OutputDevice
import time
button = Button(18, pull_up=True)
garage_door = OutputDevice(4, active_high=True, initial_value=False)
# Script for reading from the GPIO pin the magnet sensor value

garage_door.on()
print(garage_door.value)
time.sleep(1)
garage_door.off()
print(garage_door.value)

'''
def main():
    while (1):
        if button.is_pressed:
            print("switch is open")
        else:
            print("switch is closed")
        time.sleep(0.5)
'''
