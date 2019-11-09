#!/bin/bash

set -e

energy_root=$(cd $(dirname ${0})/../../;pwd)

$energy_root/IoTjs/tools/build.py                                                           \
  --target-arch arm                                                                         \
  --target-os linux                                                                         \
  --target-board rpi2                                                                       \
  --buildtype release                                                                       \
  --external-module=$energy_root/SenseHat/sense_hat_module                                  \
  --cmake-param=-DENABLE_MODULE_SENSE_HAT_MODULE=ON                                         \
  --external-lib sense-hat                                                                  \
  --external-lib pthread                                                                    \
  --external-lib RTIMULib                                                                   \
  --external-lib wiringPi

#   --external-module=$energy_root/scripts/communication_helpers/communication_helpers_module \
#   --cmake-param=-DENABLE_MODULE_COMMUNICATION_HELPERS_MODULE=ON                             \
