import subprocess
from pynput.keyboard import Controller, Key

# Create an instance of the keyboard controller
keyboard = Controller()

while True:

    subprocess.run(["python", "Hand_sign_module.py"])
    subprocess.run(["python", "mouse_pointer.py"])

