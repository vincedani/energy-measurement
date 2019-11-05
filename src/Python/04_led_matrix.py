#!/usr/bin/env python3

from scripts.communication_helpers.communication_helper import Command, send_message

from sense_hat import SenseHat
sense = SenseHat()

B = (102, 51, 0)
b = (0, 0, 255)
S = (205,133,63)
W = (255, 255, 255)

pixels = [
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, S, S, S, S, S, S, B,
    S, S, S, S, S, S, S, S,
    S, W, b, S, S, b, W, S,
    S, S, S, B, B, S, S, S,
    S, S, B, S, S, B, S, S,
    S, S, B, B, B, B, S, S
]

sense.clear()

send_message(Command.START, 'LED_show_message')
sense.show_message('TEST')
send_message(Command.STOP, 'LED_show_message')

sense.clear()

send_message(Command.START, 'LED_show_letter')
sense.show_letter('A')
send_message(Command.STOP, 'LED_show_letter')

sense.clear()

send_message(Command.START, 'LED_set_pixels')
sense.set_pixels(pixels)
send_message(Command.STOP, 'LED_set_pixels')