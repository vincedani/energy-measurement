#!/usr/bin/env python3

import threading, serial, sys
import sched, time, datetime
from enum import Enum

class Command(Enum):
  START     = 1
  STOP      = 2
  TERMINATE = 3

class LogLevel(Enum):
  INFO =  1
  ERROR = 2

port = '/dev/ttyS0'
baud_rate = 115200
timeout = 1

scheduler = sched.scheduler(time.time, time.sleep)
serial_port = serial.Serial(port, baud_rate, timeout=timeout)

is_measurement_running = False
current_message = ''

# Logging function
# TODO: When this script will be an Unix service, change logger to
#       work with it.
def log(level : LogLevel, message: str):
  print('{} [{}] {}'
    .format(datetime.datetime.now().strftime('%H:%M:%S.%f'),
            level.name,
            message))

def send_message(msg : str):
  if serial_port.is_open:
    serial_port.write('{}\n'.format(msg).encode())

def handle_error(level : LogLevel, message: str):
  if level == LogLevel.ERROR:
    send_message(message)

  log(level, message)

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

      global is_measurement_running
      global current_message

      command = Command(dictionary.get('command'))

      if command == Command.START:
        if is_measurement_running:
          is_measurement_running = False
          handle_error(LogLevel.ERROR, 'Duplicated request: Measurement has already started.')

        else:
          current_message = dictionary.get('msg')
          is_measurement_running = True

      elif command == Command.STOP:
        is_measurement_running = False

        msg = dictionary.get('msg')
        if current_message != msg:
          handle_error(LogLevel.ERROR, 'Invalid measurement was stopped.')

      # The terminate is for local testing
      # Exiting from the thead allows exiting from script with CTRL+C
      elif command == Command.TERMINATE:
        handle_error(LogLevel.INFO, 'Serial port listener has terminated.')
        sys.exit(0)

thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.start()

if __name__ == "__main__":
   scheduler.enter(0, 2, measure_energy, ())
   scheduler.run()
