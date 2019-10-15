# Using benchmarks from thesis

Clone this project to the Raspberry Pi.

```sh
cd ~
git clone https://github.com/vincedani/energy-measurement.git
```

## Sysbench

Install the benchmark with the following command:

```sh
sudo apt install sysbench
$ sysbench --version
sysbench 0.4.12
```

The [run_sysbench.sh](../scripts/benchmark_runners/run_sysbench.sh) script runs the benchmark with different parameters. It communicates with the energy-measurement service between runs.

```sh
./scripts/benchmark_runners/run_sysbench.sh
```

## Polybench

Download the source from the official [link](http://web.cse.ohio-state.edu/~pouchet.2/software/polybench/download/polybench-c-3.2.tar.gz). Decompress it and compile the application with the following command:

```sh
wget http://web.cse.ohio-state.edu/~pouchet.2/software/polybench/download/polybench-c-3.2.tar.gz

tar xvzf polybench-c-3.2.tar.gz
rm polybench-c-3.2.tar.gz

cd polybench-c-3.2
mkdir build && cd build
~/energy-measurement/scripts/benchmark_runners/polybench_build.sh ./
```

Run benchmarks:

```sh
~/energy-measurement/scripts/benchmark_runners/polybench_run.sh ./
```

## CoreMark Pro
