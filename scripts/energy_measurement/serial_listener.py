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

from pymongo import MongoClient

# uri = "mongodb://<connection-string>"
# client = MongoClient(uri)

# db = client.energyconsumption
# collection = db.consumption

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
ina.configure(bus_adc=ina.ADC_9BIT,
              shunt_adc=ina.ADC_9BIT)

sensor_data = []
start_time = datetime.datetime.now()

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
        'time': str(datetime.datetime.now() - start_time),
        'voltage': ina.voltage(),
        'current': ina.current(),
        'power': ina.power()
      })

    except DeviceRangeError as e:
      # Current out of device range with specified shunt resister
      handle_error(LogLevel.INFO, e)

  scheduler.enter(0.0005, 0, measure_energy, ())

def save_data():
  global sensor_data

  sd = copy.deepcopy(sensor_data)
  sensor_data = []
  file_name = '{}_{}'.format(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f'), current_message)

  # try:
  #   collection.insert_one({
  #     'name' : file_name,
  #     'consumption': sd
  #   })
  # except Exception as e:
  #   handle_error(LogLevel.ERROR, 'MongoDB error {}'.format(str(e)))

  path = '/home/pi/work/measurement_logs/{}.csv'.format(file_name)

  with open(path, 'w') as outfile:
    outfile.write('TimeStamp, Voltage (V), Current (mA), Power (mW)\n')
    for data in sd:
      outfile.write('{},{:.3f},{:.3f},{:.3f}\n'.format(
          data.get('time'),
          data.get('voltage'),
          data.get('current'),
          data.get('power')
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
      global start_time

      command = Command(dictionary.get('command'))

      if command == Command.START:
        if is_measurement_running:
          is_measurement_running = False
          handle_error(LogLevel.ERROR,
                       'Duplicated request: Measurement has already started ({}). Terminate.'.format(current_message))

        else:
          current_message = dictionary.get('msg')
          start_time = datetime.datetime.now()
          is_measurement_running = True

      elif command == Command.STOP:
        is_measurement_running = False

        msg = dictionary.get('msg')
        if current_message != msg:
          handle_error(LogLevel.ERROR,
                       'Invalid measurement was stopped: {}. The running session ({}) is dropped.'.format(msg, current_message))
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
