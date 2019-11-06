#!/usr/bin/env python3

from scripts.communication_helpers.communication_helper import Command, send_message

from sense_hat import SenseHat
sense = SenseHat()

for _ in range(10):
  send_message(Command.START, 'temperature_from_pressure')
  temperature_from_pressure = sense.get_temperature_from_pressure()
  send_message(Command.STOP, 'temperature_from_pressure')

  send_message(Command.START, 'temperature_from_humidity')
  temperature_from_humidity = sense.get_temperature_from_humidity()
  send_message(Command.STOP, 'temperature_from_humidity')

  send_message(Command.START, 'pressure')
  pressure = sense.get_pressure()
  send_message(Command.STOP, 'pressure')

  send_message(Command.START, 'humidity')
  humidity = sense.get_humidity()
  send_message(Command.STOP, 'humidity')
