#!/bin/bash

set -e

energy_root=$(cd $(dirname ${0})/../../;pwd)
csv_folders=$@

for folder in $csv_folders
do
  csv_files=$(ls -1 $folder)

  for file in $csv_files
  do
    file_list+=($folder/$file)
  done

done

$energy_root/scripts/tools/plot_results.py --statistics ${file_list[@]}
