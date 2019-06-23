#!/usr/bin/env python3

import threading, serial, sys
import sched, time, datetime
from enum import Enum

class Command(Enum):
  START     = 1
  STOP      = 2
  TERMINATE = 3

port = '/dev/ttyS0'
baud_rate = 115200
timeout = 1

scheduler = sched.scheduler(time.time, time.sleep)
serial_port = serial.Serial(port, baud_rate, timeout=timeout)

is_measurement_running = False
current_message = ''

# This function should do the measurement.
def measure_energy():
  if is_measurement_running:
    print('[{}] Measurement!'.format(current_message))
  else:
    print("Idle")

  scheduler.enter(1, 2, measure_energy, ())

# This fution listens to the serial console in a separate thread
# and controls the measurement process.
def read_from_port(ser):
  while True:
    reading = ser.readline().decode()
    if reading:
      dictionary = eval(reading)

      global current_message
      current_message = dictionary.get('msg')

      command = Command(dictionary.get('command'))
      global is_measurement_running

      if command == Command.START:
        is_measurement_running = True
      elif command == Command.STOP:
        is_measurement_running = False

      # The terminate is for local testing
      # Exiting from the thead allows exiting from script with CTRL+C
      elif command == Command.TERMINATE:
        sys.exit(0)

thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.start()

if __name__ == "__main__":
   scheduler.enter(0, 2, measure_energy, ())
   scheduler.run()
