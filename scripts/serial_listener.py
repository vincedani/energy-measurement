#!/usr/bin/env python3

import threading
import serial
import sys
import copy
import sched
import time
import datetime
import os
import logging

from enum import Enum
from ina219 import INA219
from ina219 import DeviceRangeError
from systemd import journal


class Command(Enum):
  START     = 1
  STOP      = 2
  TERMINATE = 3

class LogLevel(Enum):
  INFO =  1
  ERROR = 2

# Communication through serial port
port = '/dev/ttyS0'
baud_rate = 115200
timeout = 1

serial_port = serial.Serial(port, baud_rate, timeout=timeout)

# Measurement helpers
scheduler = sched.scheduler(time.time, time.sleep)
is_measurement_running = False
current_message = ''

# INA219 Configuration
SHUNT_OHMS = 0.1
SENSOR_ADDRESS = 0x40

# Logger configuration
logger = logging.getLogger('energy')
logger.addHandler(journal.JournaldLogHandler())
logger.setLevel(logging.INFO)

ina = INA219(SHUNT_OHMS, address=SENSOR_ADDRESS)
ina.configure(bus_adc=ina.ADC_12BIT,
              shunt_adc=ina.ADC_12BIT)

sensor_data = []

# Logger function
def log(level : LogLevel, message: str):
  if level == LogLevel.ERROR:
    logger.error(message)
  else:
    logger.info(message)

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
    try:
      sensor_data.append({
        't': datetime.datetime.now().strftime('%H:%M:%S.%f'),
        'u': ina.voltage(),
        'i': ina.current(),
        'p': ina.power()
      })

    except DeviceRangeError as e:
      # Current out of device range with specified shunt resister
      handle_error(LogLevel.INFO, e)

  scheduler.enter(0.015, 0, measure_energy, ())

def save_data():
  global sensor_data

  sd = copy.deepcopy(sensor_data)
  sensor_data = []

  file_name = '/home/pi/work/measurement_logs/{}_{}.csv'.format(
    datetime.datetime.now().strftime('%H_%M_%S_%f'),
    current_message)

  with open(file_name, 'w') as outfile:
    outfile.write('TimeStamp, Voltage (V), Current (mA), Power (mW)\n')
    for data in sd:
      outfile.write('{},{:.3f},{:.3f},{:.3f}\n'.format(
          data.get('t'),
          data.get('u'),
          data.get('i'),
          data.get('p')
      ))

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
          handle_error(LogLevel.ERROR,
                       'Duplicated request: Measurement has already started ({}). Terminate.'.format(current_message))

        else:
          current_message = dictionary.get('msg')
          is_measurement_running = True

      elif command == Command.STOP:
        is_measurement_running = False

        msg = dictionary.get('msg')
        if current_message != msg:
          handle_error(LogLevel.ERROR,
                       'Invalid measurement was stopped: {}. The running session ({}) is dropped.'.format(msg, current_message))
          global sensor_data
          sensor_data = []
        else:
          save_data()

      # The terminate is for local testing
      # Exiting from the thead allows exiting from script with CTRL+C
      elif command == Command.TERMINATE:
        handle_error(LogLevel.INFO, 'Serial port listener has terminated.')
        sys.exit(0)

thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.start()

if __name__ == "__main__":
  scheduler.enter(0, 0, measure_energy, ())
  scheduler.run()
