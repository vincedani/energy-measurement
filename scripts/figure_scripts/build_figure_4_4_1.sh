#!/bin/bash

set -e

energy_root=$(cd $(dirname ${0})/../../;pwd)
src_folder=$energy_root/scripts/figure_scripts/
build=$energy_root/build

file=figure_4_4_1

for optlevel in "O0" "O1" "O2" "O3" "Os"
do
  g++ $src_folder/$file.cpp -o $build/${optlevel}_${file} -$optlevel \
    $energy_root/scripts/communication_helpers/CommunicationHelper.h \
    $energy_root/scripts/communication_helpers/CommunicationHelper.c \
    -lwiringPi
done
