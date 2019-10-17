#!/bin/bash

set -e

energy_root=$(cd $(dirname ${0})/../../;pwd)
server_ip=$1

$energy_root/scripts/tools/control_measurement.py start iperf3

iperf3 -c $server_ip -t 30

$energy_root/scripts/tools/control_measurement.py stop iperf3
