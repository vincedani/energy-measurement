#!/usr/bin/env python3

from scripts.communication_helpers.communication_helper import Command, send_message

import sys
import signal
from sense_hat import SenseHat
from evdev import InputDevice, list_devices, ecodes

sense = SenseHat()

def signal_handler():
  raise Exception('timeout')

if __name__ == "__main__":
  for dev in [InputDevice(fn) for fn in list_devices()]:
    if dev.name == 'Raspberry Pi Sense HAT Joystick':
        break

  signal.signal(signal.SIGALRM, signal_handler)
  signal.alarm(10)

  try:
    send_message(Command.START, 'joystick_event_loop')

    for event in dev.read_loop():
      if event.type == ecodes.EV_KEY:
        pass

  except:
    send_message(Command.STOP, 'joystick_event_loop')
