#!/usr/bin/env python3

import os
import sys
import serial
import time
from enum import Enum

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

    response = serial_port.readline().decode()
    if response:
      print('[ERROR] Request: {}. Response: {} '.format(message, response))
