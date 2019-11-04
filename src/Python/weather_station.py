#!/usr/bin/env python3

import os
import sys
import copy
import time
import sched
import threading
import datetime
import logging
import sqlite3

from enum import Enum
from systemd import journal

FIVE_MINUTES_IN_SEC = 300
THIRTY_MINUTES_IN_SEC = 1800
SIXTY_MINUTES_IN_SEC = 3600

DB_PATH = os.path.join(os.path.dirname(__file__), '../weather_station.db')
sense = SenseHat()
low_light_mode = False

class LogLevel(Enum):
  INFO =  1
  ERROR = 2

class Measurement:
  def __init__(self, timestamp, temperature, humidity, pressure):
    self.timestamp = timestamp
    self.temperature = temperature
    self.humidity = humidity
    self.pressure = pressure

# Measurement helpers
scheduler = sched.scheduler(time.time, time.sleep)

# Logger configuration
logger = logging.getLogger('weather_station')
logger.addHandler(journal.JournaldLogHandler())
logger.setLevel(logging.INFO)

sensor_data = []

# Logger function
def log(level : LogLevel, message : str):
  if level == LogLevel.ERROR:
    logger.error(message)
  else:
    logger.info(message)


def handle_error(level : LogLevel, message : str):
  log(level, message)


def save_data(data : Measurement):
  try:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    command = 'insert into Measurements (TimeStamp, Temperature, Humidity, Pressure) ' \
          + 'values (?, ?, ?, ?)'

    cursor.execute(command, (data.timestamp, data.temperature, data.humidity, data.pressure))
    connection.commit()
  except sqlite3.Error as e:
    handle_error(LogLevel.ERROR, e)


def measure_environment():
  temperature = (sense.get_temperature_from_pressure() + sense.get_temperature_from_humidity()) / 2
  print('Measure')
  # TODO: Do something useful.
  scheduler.enter(FIVE_MINUTES_IN_SEC, 0, measure_environment, ())

def synchronize_with_server():
  print ('Sync')
  # TODO: Do something useful.
  scheduler.enter(SIXTY_MINUTES_IN_SEC, 1, synchronize_with_server, ())

def fetch_data_from_accuweather():
  print ('Fetch')
  # TODO: Do something useful.
  scheduler.enter(THIRTY_MINUTES_IN_SEC, 1, fetch_data_from_accuweather, ())

# thread = threading.Thread(target=read_from_port, args=(serial_port,))
# thread.start()

if __name__ == "__main__":
  scheduler.enter(0, 0, measure_environment, ())
  scheduler.enter(THIRTY_MINUTES_IN_SEC, 1, fetch_data_from_accuweather, ())

  # Delay needed (60 + 10 min) here, because if the data fetching and the
  # syncronization are running in the same time then the energy measurement
  # breaks and only the first is recorded.
  scheduler.enter(SIXTY_MINUTES_IN_SEC + 10, 1, synchronize_with_server, ())

  scheduler.run()
