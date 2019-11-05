#!/usr/bin/env python3

from scripts.communication_helpers.communication_helper import Command, send_message

import sqlite3
import requests
import json

API_ENDPOINT = 'http://192.168.2.178/weather/add'
DB_PATH = os.path.join(os.path.dirname(__file__), '../weather_station.db')

# AccuWeather
AW_API_KEY      = ''
AW_API_KEY_PATH = os.path.join(os.path.dirname(__file__), '../accuweather_api_key.txt')
AW_SZEGED_URL   = 'http://dataservice.accuweather.com/currentconditions/v1/187706'

def http_post():
  connection = sqlite3.connect(DB_PATH)
  cursor = connection.cursor()

  command = 'select * from Measurements order by ID desc limit 5'

  cursor.execute(command)
  rows = cursor.fetchall()

  send_message(Command.START, 'http_post')

  data = []
  headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
  for row in rows:
    record = {
      'TimeStamp'   : row[1],
      'Temperature' : row[2],
      'Humidity'    : row[3],
      'Pressure'    : row[4]
    }
    data.append(record)

  response = requests.post(url = API_ENDPOINT, json = data, headers = headers)

  send_message(Command.STOP, 'http_post')


def http_get():
  with open(AW_API_KEY_PATH, 'r') as file:
    AW_API_KEY = file.read()

  send_message(Command.START, 'http_get')
  body = {
    'apikey' : AW_API_KEY,
    'details' : 'true'
  }

  response = requests.get(url = AW_SZEGED_URL, params = body)
  response_json = response.json()[0]

  temperature = response_json['Temperature']['Metric']['Value']
  humidity = response_json['RelativeHumidity']
  pressure = response_json['Pressure']['Metric']['Value']

  send_message(Command.STOP, 'http_get')

if __name__ == "__main__":
  http_post()
  http_get()
