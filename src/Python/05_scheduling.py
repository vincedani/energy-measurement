#!/usr/bin/env python3

from scripts.communication_helpers.communication_helper import Command, send_message

import time
import sched
import datetime

scheduler = sched.scheduler(time.time, time.sleep)
start_time = ''

def function_1():
  if datetime.datetime.now() - start_time < datetime.timedelta(seconds=10):
    scheduler.enter(1, 0, function_1, ())

if __name__ == "__main__":
  send_message(Command.START, 'scheduling')

  start_time = datetime.datetime.now()
  scheduler.enter(0, 0, function_1, ())
  scheduler.run()

  send_message(Command.STOP, 'scheduling')
