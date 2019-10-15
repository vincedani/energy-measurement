#!/bin/bash

energy_root=$(cd $(dirname ${0})/../../;pwd)
benchmark_dir=$1
benchmarks=$(ls -1 $benchmark_dir)

echo $energy_root
for benchmark in $benchmarks
do
  # start energy measurement
  runnable=${benchmark_dir}/${benchmark}
  $runnable
  # stop energy measurement
done
