#!/bin/bash

set -e

project_root=$(cd $(dirname ${0})/../;pwd)

$project_root/scripts/tools/control_measurement.py start test_012
sleep 3
$project_root/scripts/tools/control_measurement.py stop test_012