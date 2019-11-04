#!/usr/bin/env python3

import os
import time
import sched
import datetime
import sqlite3
import requests
import json

from enum import Enum
from sense_hat import SenseHat

FIVE_MINUTES_IN_SEC = 300
THIRTY_MINUTES_IN_SEC = 1800
SIXTY_MINUTES_IN_SEC = 3600

# Local server
API_ENDPOINT = 'http://192.168.2.178/weather/add'

# AccuWeater
AW_API_KEY = ''
AW_API_KEY_PATH = os.path.join(os.path.dirname(__file__), '../accuweather_api_key.txt')
AW_SZEGED_URL   = 'http://dataservice.accuweather.com/currentconditions/v1/187706'
AW_TEMPERATURE  = 0
AW_HUMIDITY     = 0
AW_PRESSURE     = 0

DB_PATH = os.path.join(os.path.dirname(__file__), '../weather_station.db')

# Seting up
sense = SenseHat()
low_light_mode = False

# Measurement helpers
scheduler = sched.scheduler(time.time, time.sleep)

class LogLevel(Enum):
  INFO =  1
  ERROR = 2

class Measurement:
  def __init__(self, timestamp, temperature, humidity, pressure):
    self.timestamp = timestamp
    self.temperature = temperature
    self.humidity = humidity
    self.pressure = pressure


# Logger function
def log(level : LogLevel, message : str):
  if level == LogLevel.ERROR:
    print('[ERROR] {} | {}'.format(datetime.datetime.now().strftime('%H:%M:%S.%f'), message))
  else:
    print('[INFO] {} | {}'.format(datetime.datetime.now().strftime('%H:%M:%S.%f'), message))


def save_data(data : Measurement):
  try:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    command = 'insert into Measurements (TimeStamp, Temperature, Humidity, Pressure) ' \
          + 'values (?, ?, ?, ?)'

    cursor.execute(command, (data.timestamp, data.temperature, data.humidity, data.pressure))
    connection.commit()
  except sqlite3.Error as e:
    log(LogLevel.ERROR, e)


def measure_environment():
  temperature = (sense.get_temperature_from_pressure() + sense.get_temperature_from_humidity()) / 2
  humidity = sense.get_humidity()
  pressure = sense.get_pressure()

  measurement = Measurement(datetime.datetime.now().strftime('%H:%M:%S.%f'),
                            round(temperature, 3),
                            round(humidity, 3),
                            round(pressure, 3))

  save_data(measurement)
  scheduler.enter(FIVE_MINUTES_IN_SEC, 0, measure_environment, ())


def synchronize_with_server():
  try:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    command = 'select * from Measurements order by ID desc limit 5'

    cursor.execute(command)
    rows = cursor.fetchall()
    send_request(rows)

  except Exception as e:
    log(LogLevel.ERROR, e)

  scheduler.enter(SIXTY_MINUTES_IN_SEC, 1, synchronize_with_server, ())


def send_request(data_rows):
  data = []
  headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
  for row in data_rows:
    record = {
      'TimeStamp'   : row[1],
      'Temperature' : row[2],
      'Humidity'    : row[3],
      'Pressure'    : row[4]
    }
    data.append(record)

  response = requests.post(url = API_ENDPOINT, json = data, headers = headers)


def fetch_data_from_accuweather():
  body = {
    'apikey' : AW_API_KEY,
    'details' : 'true'
  }

  response = requests.get(url = AW_SZEGED_URL, params = body)
  response_json = response.json()[0]

  temperature = response_json['Temperature']['Metric']['Value']
  humidity = response_json['RelativeHumidity']
  pressure = response_json['Pressure']['Metric']['Value']

  scheduler.enter(THIRTY_MINUTES_IN_SEC, 1, fetch_data_from_accuweather, ())

if __name__ == "__main__":
  scheduler.enter(0, 0, measure_environment, ())
  # Delay needed (60 + 10 min) here, because if the data fetching and the
  # syncronization are running in the same time then the energy measurement
  # breaks and only the first is recorded.
  scheduler.enter(SIXTY_MINUTES_IN_SEC + 600, 1, synchronize_with_server, ())

  with open(AW_API_KEY_PATH, 'r') as file:
    AW_API_KEY = file.read()

  scheduler.enter(30, 1, fetch_data_from_accuweather, ())
  scheduler.run()
