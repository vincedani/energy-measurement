#!/usr/bin/env python3

import serial, time
from enum import Enum

class Command(Enum):
  START     = 1
  STOP      = 2
  TERMINATE = 3

port = '/dev/ttyS0'
baud_rate = 115200
timeout = 1

serial_port = serial.Serial(port, baud_rate, timeout=timeout)

def send_message(command : Command, msg : str):
  if serial_port.is_open:
    message = { 'command' : command.value, 'msg': msg }
    serial_port.write('{}\n'.format(message).encode())


time.sleep(2)
send_message(Command.START, 'test_sender.py:24')

time.sleep(4)
send_message(Command.STOP, 'test_sender.py:27')

time.sleep(0.5)
send_message(Command.TERMINATE, 'test_sender.py:30')
