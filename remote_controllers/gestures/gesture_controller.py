"""
    gesture_controller.py

    This file implements the code needed use a microbit and its gestures
    to control the movement of the microbit_robot over the radio interface.

    It uses the display to indicate the current current direction.
    An "X" means stopped

    Point the USB connector towards the floor = Forward
    Point the USB connector towards the ceiling = Reverse
    Point Button A towards the ceiling = Turn Right
    Pint Button A towards the floor = Turn Left
    Push Button A = Spin left
    Push Button B = Spin Right

    License: The MIT License (MIT)

    Copyright (c) 2018 Alan Yorinks

"""

from microbit import *
import radio

# the last gesture detected
last_gesture = ''

def send_command(cmd):
    """
    This function sends a command to the radio.
    :param cmd: Command string
    :return:
    """
    radio.on()
    radio.send(cmd)
    sleep(100)
    radio.off()

# the main loop
while True:
    # get the current gesture
    gesture = accelerometer.current_gesture()

    # if either button is pressed, translate this to
    # a pseudo gesture
    if button_a.is_pressed():
        gesture = 'spin_left'
    if button_b.is_pressed():
        gesture = 'spin_right'

    # if this gesture is different than the last,
    # build the command string and transmit it over the radio.
    if not last_gesture == gesture:
        last_gesture = gesture
        if gesture == 'down':
            display.show(Image.ARROW_N)
            send_command('fwd')
        elif gesture == 'up':
            display.show(Image.ARROW_S)
            send_command('rev')
        elif gesture == 'left':
            display.show(Image.ARROW_W)
            send_command('left')
        elif gesture == 'right':
            display.show(Image.ARROW_E)
            send_command('right')
        elif gesture == 'spin_left':
            display.show(Image.ARROW_SW)
            send_command('spin_left')
        elif gesture == 'spin_right':
            display.show(Image.ARROW_SE)
            send_command('spin_right')
        else:
            display.show(Image.NO)
            send_command('stop')
