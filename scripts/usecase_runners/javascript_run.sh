#!/bin/bash

set -e

energy_root=$(cd $(dirname ${0})/../../;pwd)
iotjs_bin=$energy_root/build/iotjs/arm-linux/release/bin/iotjs

echo "Running JavaScript tests..."

$iotjs_bin $energy_root/src/JavaScript/01_sensors.js
$iotjs_bin $energy_root/src/JavaScript/02_sqlite.js
$iotjs_bin $energy_root/src/JavaScript/03_http.js
$iotjs_bin $energy_root/src/JavaScript/04_led_matrix.js
$iotjs_bin $energy_root/src/JavaScript/05_scheduling.js

echo "Done"
