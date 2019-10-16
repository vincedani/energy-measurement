#!/bin/bash

set -e

energy_root=$(cd $(dirname ${0})/../../;pwd)
benchmark_dir=$1
benchmarks=$(ls -1 $benchmark_dir)

for benchmark in $benchmarks
do
  $energy_root/scripts/tools/control_measurement.py start $benchmark

  runnable=${benchmark_dir}/${benchmark}
  $runnable

  $energy_root/scripts/tools/control_measurement.py stop $benchmark
done
