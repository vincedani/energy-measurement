#!/usr/bin/env python3

import time
import sched

scheduler = sched.scheduler(time.time, time.sleep)

def function_1():
  scheduler.enter(1, 0, function_1, ())

if __name__ == "__main__":
  scheduler.enter(0, 0, function_1, ())
  scheduler.run()