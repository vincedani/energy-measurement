#!/bin/bash

set -e

energy_root=$(cd $(dirname ${0})/../../;pwd)
iotjs_bin=$energy_root/build/iotjs/arm-linux/release/bin/iotjs

for run_cnt in {1..10}
do
  PYTHONOPTIMIZE=1 $energy_root/scripts/figure_scripts/figure_4_4_2.py 1400
  sync
done

for run_cnt in {1..10}
do
  $iotjs_bin $energy_root/scripts/figure_scripts/figure_4_4_3.js 1400
  sync
done

for run_cnt in {1..10}
do
  $energy_root/build/O0_figure_4_4_1 1400
  sync

  $energy_root/build/O1_figure_4_4_1 1400
  sync

  $energy_root/build/O2_figure_4_4_1 1400
  sync

  $energy_root/build/O3_figure_4_4_1 1400
  sync

  $energy_root/build/Os_figure_4_4_1 1400
  sync

done