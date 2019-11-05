#!/usr/bin/env python3

import sys

from sense_hat import SenseHat
from evdev import InputDevice, list_devices, ecodes

sense = SenseHat()

for dev in [InputDevice(fn) for fn in list_devices()]:
  if dev.name == 'Raspberry Pi Sense HAT Joystick':
      break


try:
  send_message(Command.START, 'joystick_event_loop')

  for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
      pass

  send_message(Command.STOP, 'joystick_event_loop')
except KeyboardInterrupt:
    sys.exit()