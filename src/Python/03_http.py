#!/usr/bin/env python3

from scripts.communication_helpers.communication_helper import Command, send_message

import os
import requests
import json

API_ENDPOINT = 'http://192.168.2.58/MockServer/api/weather/'

def http_post():
  data = [
    { 'TimeStamp' : '23:33:14.695226', 'Temperature' : 24.893, 'Humidity' : 56.576, 'Pressure' : 998.634 },
    { 'TimeStamp' : '23:33:33.805037', 'Temperature' : 24.963, 'Humidity' : 56.488, 'Pressure' : 998.640 },
    { 'TimeStamp' : '23:34:02.239622', 'Temperature' : 25.177, 'Humidity' : 55.715, 'Pressure' : 998.687 },
    { 'TimeStamp' : '23:34:54.227033', 'Temperature' : 24.939, 'Humidity' : 55.843, 'Pressure' : 998.686 },
    { 'TimeStamp' : '23:39:44.063628', 'Temperature' : 24.980, 'Humidity' : 55.676, 'Pressure' : 998.705 }
  ]

  headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
  send_message(Command.START, 'http_post')

  try:
    response = requests.post(url = API_ENDPOINT, json = data, headers = headers)
  except Exception as e:
    print(e)

  send_message(Command.STOP, 'http_post')


def http_get():
  send_message(Command.START, 'http_get')

  url = '{}/{}'.format(API_ENDPOINT, '12')
  response = requests.get(url = url)
  response_json = response.json()

  send_message(Command.STOP, 'http_get')

if __name__ == "__main__":
  for index in range(10):
    http_post()
    http_get()
