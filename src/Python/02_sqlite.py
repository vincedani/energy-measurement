#!/usr/bin/env python3

from scripts.communication_helpers.communication_helper import Command, send_message

import os
import sqlite3
import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '../weather_station.db')

def insert_record():
  timestamp   = datetime.datetime.now().strftime('%H:%M:%S.%f')
  temperature = 25.072
  humidity    = 56.19
  pressure    = 998.646

  send_message(Command.START, 'save_record_sqlite3')

  connection = sqlite3.connect(DB_PATH)
  cursor = connection.cursor()

  command = 'insert into Measurements (TimeStamp, Temperature, Humidity, Pressure) ' \
        + 'values (?, ?, ?, ?)'

  cursor.execute(command, (timestamp, temperature, humidity, pressure))
  connection.commit()
  connection.close()

  send_message(Command.STOP, 'save_record_sqlite3')


def query_records():
  send_message(Command.START, 'query_record_sqlite3')

  connection = sqlite3.connect(DB_PATH)
  cursor = connection.cursor()

  command = 'select * from Measurements order by ID desc limit 5'

  cursor.execute(command)
  rows = cursor.fetchall()
  connection.close()

  send_message(Command.STOP, 'query_record_sqlite3')

if __name__ == "__main__":
  for _ in range(10):
    insert_record()
    query_records()