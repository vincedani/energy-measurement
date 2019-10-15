#!/bin/bash

set -e

polybench_dir=$1
benchmarks=$(cat $polybench_dir/utilities/benchmark_list)

for benchmark in $benchmarks
do
  file=$(basename $benchmark)
  folder=$(dirname $benchmark)
  name=$(echo "$file" | cut -f 1 -d '.')

  gcc                                    \
    -I $polybench_dir/utilities          \
    -I $polybench_dir/folder             \
    $polybench_dir/$benchmark            \
    $polybench_dir/utilities/polybench.c \
    -o $name                             \
    -lm
done
