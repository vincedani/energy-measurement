#!/usr/bin/env python3

import pickle
import sched, time, datetime
from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.022
SENSOR_ADDRESS = 0x40

s = sched.scheduler(time.time, time.sleep)
ina = INA219(SHUNT_OHMS, address=SENSOR_ADDRESS)
ina.configure()

start_time = datetime.datetime.now()
sensor_data = []

def export_data():
  with open('mybinary.csv', 'wb') as outfile:
    outfile.write('TimeStamp, Voltage (V), Current (mA), Power (mW)\n'.encode())
    for data in sensor_data:
      pickle.dump('{},{},{},{}\n'
        .format(
          data.get('t'),
          data.get('u'),
          data.get('i'),
          data.get('p')
        ),
        outfile)

def read():
  try:
    sensor_data.append({
      't': datetime.datetime.now().strftime('%H:%M:%S.%f'),
      'u': ina.voltage(),
      'i': ina.current(),
      'p': ina.power()
    })

    if ((datetime.datetime.now() - start_time)).seconds < 10: # 3600:
      s.enter(0.020, 2, read, ())
    else:
      export_data()
  except DeviceRangeError as e:
    # Current out of device range with specified shunt resister
    print(e)

if __name__ == "__main__":
   s.enter(0, 2, read, ())
   s.run()
