#!/usr/bin/env python3

from scripts.communication_helpers.communication_helper import Command, send_message

import time
from sense_hat import SenseHat

sense = SenseHat()

W = (255, 255, 255)
B = (0, 0, 0)

for _ in range(10):

    # Show string message
    sense.clear()
    send_message(Command.START, 'LED_show_message')
    message = 'TEST'
    for i in range(len(message)):
        sense.show_letter(message[i])
        time.sleep(1)
    send_message(Command.STOP, 'LED_show_message')

    # Show an 'A' letter
    sense.clear()
    send_message(Command.START, 'LED_show_letter')
    sense.show_letter('A')
    time.sleep(3)
    send_message(Command.STOP, 'LED_show_letter')

    # Light up pixels for more accurate measurement.
    sense.clear()
    pixels = [
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B
    ]
    for constraint in range(9):
        for i in range(constraint):
            for j in range(constraint):
                pixels[i * 8 + j] = W

        measurement_message = 'LED_set_pixels_{}'.format(constraint)
        send_message(Command.START, measurement_message)
        sense.set_pixels(pixels)
        time.sleep(3)
        send_message(Command.STOP, measurement_message)
