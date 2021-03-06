#!/usr/bin/env python3

import os
import argparse
import csv
import datetime
import random
import numpy as np
import matplotlib.pyplot as plt
import sys

from statistics import mean
from scipy.ndimage.filters import gaussian_filter1d

PLOT_COLORS = ['b', 'g', 'r', 'c', 'm', 'k']
FILE_EXTENSION_LENGTH = 4
FILE_TIMESTAMP_LENGTH = 16
SHORT_MEASUREMENT_TIC_COUNT = 450

EPOCH = datetime.datetime(1900, 1, 1, 0, 0)

def load_input_file(input_file):
  time_values = []
  voltage_values = []
  current_values = []
  power_values = []

  with open(input_file) as csvfile:
    lines = csv.reader(csvfile, delimiter=',')

    for line in lines:
      if line[0] == 'TimeStamp':
        continue

      time_values.append(datetime.datetime.strptime(line[0], '%H:%M:%S.%f'))
      voltage_values.append(float(line[1]))
      current_values.append(float(line[2]))
      power_values.append(float(line[3]))

  return [time_values, voltage_values, current_values, power_values]


def load_input_files(input_files):
  time_values = []
  voltage_values = []
  current_values = []
  power_values = []

  for file in input_files:
    t, u, i, p = load_input_file(file)
    time_values.append(t)
    voltage_values.append(u)
    current_values.append(i)
    power_values.append(p)

  return [time_values, voltage_values, current_values, power_values]


def show_subplots(time, voltage, current, power, args, color_index):
  subplot_columns = len(args.input)
  subplot_rows = args.current + args.voltage + (not args.no_power)
  color = PLOT_COLORS[color_index]

  plot_index = 0

  plt.suptitle(args.title, fontsize=26)
  for index in range(0, subplot_columns):
    plot_index = index + 1

    if args.interpolate:
      current_values = gaussian_filter1d(current[index], sigma=2)
      power_values = gaussian_filter1d(power[index], sigma=2)
      voltage_values = gaussian_filter1d(voltage[index], sigma=2)
    else:
      current_values = current[index]
      power_values = power[index]
      voltage_values = voltage[index]

    if args.voltage:
      plt.subplot(subplot_rows, subplot_columns, plot_index)
      plt.xticks(fontsize=16)
      plt.yticks(fontsize=16)

      if len(time[index]) < SHORT_MEASUREMENT_TIC_COUNT:
        plt.plot(time[index], voltage_values, 'o-', linewidth=2, markersize=3 ,color=color)
      else:
        plt.plot(time[index], voltage_values, color=color)

      plt.xlabel('Time (s)', fontsize=20)
      plt.ylabel('Voltage (V)', fontsize=16)
      plt.grid(True)
      plot_index += subplot_columns


    if args.current:
      plt.subplot(subplot_rows, subplot_columns, plot_index)
      plt.xticks(fontsize=16)
      plt.yticks(fontsize=16)

      if len(time[index]) < SHORT_MEASUREMENT_TIC_COUNT:
        plt.plot(time[index], current_values, 'o-', linewidth=2, markersize=3 ,color=color)
      else:
        plt.plot(time[index], current_values, color=color)

      plt.xlabel('Time (s)', fontsize=20)
      plt.ylabel('Current (mA)', fontsize=16)
      plt.grid(True)
      plot_index += subplot_columns


    if not args.no_power:
      plt.subplot(subplot_rows, subplot_columns, plot_index)
      plt.xticks(fontsize=16)
      plt.yticks(fontsize=16)

      axes = plt.gca()
      axes.set_ylim([1200,2600])

      if len(time[index]) < SHORT_MEASUREMENT_TIC_COUNT:
        plt.plot(time[index], power_values, 'o-', linewidth=2, markersize=3 ,color=color)
      else:
        plt.plot(time[index], power_values, color=color)

      plt.xlabel('Time (s)', fontsize=20)
      plt.ylabel('Power (mW)', fontsize=16)
      plt.grid(True)

  plt.subplots_adjust(left=0.06, right=0.99, bottom=0.08, top=0.93)
  plt.show()


def show_merged_plot(time, voltage, current, power, args):

  plt.suptitle(args.title, fontsize=26)
  plt.xlabel('Time (s)', fontsize=20)
  plt.ylabel('Power (mW)', fontsize=20)
  plt.xticks(fontsize=16)
  plt.yticks(fontsize=16)

  plt.grid(True)

  for index in range(0, len(args.input)):
    legend = os.path.basename(args.input[index])

    axes = plt.gca()
    axes.set_ylim([1300,1800])
    if args.interpolate:
      # power_values = gaussian_filter1d(power[index], sigma=2)
      power_values = gaussian_filter1d(power[index], sigma=4)
    else:
      power_values = power[index]

    color_index = index if index < len(PLOT_COLORS) else 0
    color = PLOT_COLORS[color_index]

    if len(time[index]) < SHORT_MEASUREMENT_TIC_COUNT:
      plt.plot(time[index], power_values, 'o-', linewidth=2, markersize=3, color=color, label=legend)
    else:
      plt.plot(time[index], power_values, color=color, label=legend, linewidth=2)

  plt.legend(prop={'size': 16})
  plt.subplots_adjust(left=0.06, right=0.99, bottom=0.08, top=0.93)
  # file_name = legend[:-FILE_EXTENSION_LENGTH]
  # plt.savefig('{}.png'.format(file_name), dpi=1000)
  plt.show()

def calculate_energy_consumption(p, t):
  deltas = []

  for index in range(0, len(p)):
    deltas.append((t[index] - EPOCH).total_seconds())

  return np.trapz(p, deltas)


def get_padding_length(length, time):
  max_length = 0
  max_delta = 0
  for index in range(0, length):
    delta = (time[index][len(time[index]) - 1 ] - time[index][0]).total_seconds()
    lenth = len(time[index])

    max_delta = delta if delta > max_delta else max_delta
    max_length = lenth if lenth > max_length else max_length

  return [max_length, max_delta]


def pad_data(time, voltage, current, power, max_length, max_delta, input_length):
  for index in range(0, input_length):
    t = time[index]
    u = voltage[index]
    i = current[index]
    p = power[index]

    if len(t) == max_length:
      continue

    t.append(EPOCH + datetime.timedelta(seconds=max_delta))
    u.append(min(u))
    i.append(min(i))
    p.append(min(p))

  return [time, voltage, current, power]


if __name__ == '__main__':
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('-c', '--current', action='store_true', default=False,
                      help='Show current values from the given CSV(s) on a subplot')
  parser.add_argument('-u', '--voltage', action='store_true', default=False,
                      help='Show voltage values from the given CSV(s) on a subplot')
  parser.add_argument('--no-power', action='store_true', default=False,
                      help='Do not show power values from the given CSV(s) on a subplot')
  parser.add_argument('-m', '--merged', action='store_true', default=False,
                      help='Show multiple measurements on the same plot.')
  parser.add_argument('-t', '--title', default='Untitled',
                      help='The title of the generated plot.')
  parser.add_argument('--statistics', action='store_true', default=False,
                      help='Print statistics from the given files instead of plotting them.')
  parser.add_argument('--interpolate', action='store_true', default=False,
                      help='Interpolate results before plotting.')
  parser.add_argument('--pad', action='store_true', default=False,
                      help='Add padding to results before plotting.')
  parser.add_argument('input', nargs='+', default=[],
                      help='Input CSV file(s) to process.')

  args = parser.parse_args()

  time, voltage, current, power = load_input_files(args.input)

  if args.pad:
    max_length, max_delta = get_padding_length(len(args.input), time)
    pad_data(time, voltage, current, power, max_length, max_delta, len(args.input))

  if not args.statistics:
    if args.merged:
      show_merged_plot(time, voltage, current, power, args)
    else:
      show_subplots(time, voltage, current, power, args, PLOT_COLORS.index('k'))

  else:
    print('Name,Length (s),Voltage (V),Current (mA),Power (mW), Energy consumption (Ws)')

    for index in range(0, len(args.input)):
      t = time[index]
      u = voltage[index]
      i = current[index]
      p = power[index]

      delta = (t[len(t) - 1 ] - t[0]).total_seconds()
      energy = calculate_energy_consumption(p, t) / 1000

      print('{:<50}, {:>10.3f}, {:>10.3f}, {:>10.3f}, {:>10.3f}, {:>10.3f}'.format(
        os.path.basename(args.input[index])[:-FILE_EXTENSION_LENGTH],
        delta,
        mean(u),
        mean(i),
        mean(p),
        energy
      ))
