#!/bin/bash

set -e

energy_root=$(cd $(dirname ${0})/../../;pwd)

## File IO benchmark
$energy_root/scripts/tools/control_measurement.py start sysbench_io_prepare
sysbench --test=fileio --file-total-size=2G prepare
$energy_root/scripts/tools/control_measurement.py stop sysbench_io_prepare

$energy_root/scripts/tools/control_measurement.py start sysbench_io_test
sysbench --test=fileio --file-total-size=2G --file-test-mode=rndrw --max-time=300 --max-requests=0 run
$energy_root/scripts/tools/control_measurement.py stop sysbench_io_test

$energy_root/scripts/tools/control_measurement.py start sysbench_io_cleanup
sysbench --test=fileio --file-total-size=2G cleanup
$energy_root/scripts/tools/control_measurement.py stop sysbench_io_cleanup

## CPU benchmark
for thread_cnt in {1..4}
do
  $energy_root/scripts/tools/control_measurement.py start sysbench_cpu_${thread_cnt}

  sysbench --test=cpu --cpu-max-prime=30000 --num-threads=$thread_cnt run

  $energy_root/scripts/tools/control_measurement.py stop sysbench_cpu_${thread_cnt}
done

## Memory benchmark
for thread_cnt in {1..4}
do
  $energy_root/scripts/tools/control_measurement.py start sysbench_memory_${thread_cnt}

  sysbench --test=memory --num-threads=4 run

  $energy_root/scripts/tools/control_measurement.py stop sysbench_memory_${thread_cnt}
done
