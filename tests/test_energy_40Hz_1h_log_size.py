#!/usr/bin/env python3

from ina219 import INA219
from ina219 import DeviceRangeError
import sched, time, datetime

SHUNT_OHMS = 0.022
SENSOR_ADDRESS = 0x40

s = sched.scheduler(time.time, time.sleep)
ina = INA219(SHUNT_OHMS, address=SENSOR_ADDRESS)
ina.configure()

start_time = datetime.datetime.now()

def read():
  try:
    print('{0},{1:.3f}, {2:.3f},{3:.3f}'
      .format(
        datetime.datetime.now().strftime('%H:%M:%S.%f'),
        ina.voltage(),
        ina.current(),
        ina.power()))

    if ((datetime.datetime.now() - start_time)).seconds < 3600:
      s.enter(0.02, 2, read, ())
  except DeviceRangeError as e:
    # Current out of device range with specified shunt resister
    print(e)

if __name__ == "__main__":
   s.enter(0, 2, read, ())
   s.run()
