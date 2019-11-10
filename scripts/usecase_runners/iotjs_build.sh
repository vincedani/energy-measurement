#!/bin/bash

set -e

energy_root=$(cd $(dirname ${0})/../../;pwd)

$energy_root/IoTjs/tools/build.py                                                           \
  --target-arch arm                                                                         \
  --target-os linux                                                                         \
  --target-board rpi2                                                                       \
  --buildtype release                                                                       \
  --builddir $energy_root/build/iotjs                                                       \
  --external-modules $energy_root/scripts/communication_helpers/communication_helpers_module,$energy_root/SenseHat/sense_hat_module,$energy_root/iotjs_modules/sleep,$energy_root/iotjs_modules/sqlite \
  --cmake-param=-DENABLE_MODULE_SENSE_HAT_MODULE=ON                                         \
  --cmake-param=-DENABLE_MODULE_COMMUNICATION_HELPERS_MODULE=ON                             \
  --cmake-param=-DENABLE_MODULE_SLEEP=ON                                                    \
  --cmake-param=-DENABLE_MODULE_SQLITE_MODULE=ON                                            \
  --external-lib sense-hat                                                                  \
  --external-lib pthread                                                                    \
  --external-lib RTIMULib                                                                   \
  --external-lib wiringPi                                                                   \
  --external-lib sqlite3
