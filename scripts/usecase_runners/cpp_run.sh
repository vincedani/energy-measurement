#!/bin/bash

set -e

energy_root=$(cd $(dirname ${0})/../../;pwd)

echo "Running C++ tests..."

$energy_root/build/01_sensors
$energy_root/build/02_sqlite
$energy_root/build/03_http
$energy_root/build/04_led_matrix
$energy_root/build/05_scheduling

echo "Done"
