#!/bin/bash

set -e

energy_root=$(cd $(dirname ${0})/../../;pwd)

echo "Running Python tests..."

$energy_root/src/Python/01_sensors.py
$energy_root/src/Python/02_sqlite.py
$energy_root/src/Python/03_http.py
$energy_root/src/Python/04_led_matrix.py
$energy_root/src/Python/05_scheduling.py

echo "Done"
