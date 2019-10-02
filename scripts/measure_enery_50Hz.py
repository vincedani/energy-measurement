#!/usr/bin/env python3

from ina219 import INA219
from ina219 import DeviceRangeError
import sched, time, datetime

SHUNT_OHMS = 0.1
SENSOR_ADDRESS = 0x40

s = sched.scheduler(time.time, time.sleep)
ina = INA219(SHUNT_OHMS, address=SENSOR_ADDRESS)
ina.configure(bus_adc=ina.ADC_128SAMP,
              shunt_adc=ina.ADC_128SAMP,
              voltage_range=ina.RANGE_16V)

def read():
  try:
    print('{},{:.3f},{:.3f},{:.3f}'
      .format(
        datetime.datetime.now().strftime('%H:%M:%S.%f'),
        ina.voltage(),
        ina.current(),
        ina.power()))

    s.enter(0.015, 0, read, ())
  except DeviceRangeError as e:
    # Current out of device range with specified shunt resister
    print(e)

if __name__ == "__main__":
  print('TimeStamp, Voltage (V), Current (mA), Power (mW)\n')
  s.enter(0, 0, read, ())
  s.run()
