#!/bin/bash

set -e

energy_root=$(cd $(dirname ${0})/../../;pwd)
src_folder=$energy_root/src/C++/
build=$energy_root/build

# 01_sensors
file=01_sensors
g++ $src_folder/$file.cpp -o $build/$file                          \
  -L$energy_root/SenseHat/build -lsense-hat                        \
  $energy_root/scripts/communication_helpers/CommunicationHelper.h \
  $energy_root/scripts/communication_helpers/CommunicationHelper.c \
  -lwiringPi

# 02_sqlite
file=02_sqlite
g++ $src_folder/$file.cpp $src_folder/$file.h -o $build/$file      \
  $energy_root/scripts/communication_helpers/CommunicationHelper.h \
  $energy_root/scripts/communication_helpers/CommunicationHelper.c \
  -lwiringPi                                                       \
  -lsqlite3

# 03_http
file=03_http
g++ $src_folder/$file.cpp -o $build/$file                          \
  $energy_root/scripts/communication_helpers/CommunicationHelper.h \
  $energy_root/scripts/communication_helpers/CommunicationHelper.c \
  -lwiringPi                                                       \
  -lcurl

# 04_led_matrix
file=04_led_matrix
g++ $src_folder/$file.cpp -o $build/$file                          \
  -L$energy_root/SenseHat/build -lsense-hat                        \
  $energy_root/scripts/communication_helpers/CommunicationHelper.h \
  $energy_root/scripts/communication_helpers/CommunicationHelper.c \
  -lwiringPi

# 05_scheduling
file=05_scheduling
g++ $src_folder/$file.cpp -o $build/$file                          \
  $energy_root/scripts/communication_helpers/CommunicationHelper.h \
  $energy_root/scripts/communication_helpers/CommunicationHelper.c \
  -lwiringPi                                                       \
  -lpthread
