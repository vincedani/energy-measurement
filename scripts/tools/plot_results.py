#!/usr/bin/env python3

import argparse
import csv
import datetime
import random
import matplotlib.pyplot as plt
from statistics import mean

PLOT_COLORS = ['b', 'g', 'r', 'c', 'm', 'k']

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

    if args.current:
      plt.subplot(subplot_rows, subplot_columns, plot_index)
      plt.plot(time[index], voltage[index], color=color)
      plt.xlabel('Time (s)', fontsize=20)
      plt.ylabel('Voltage (V)', fontsize=20)
      plt.grid(True)
      plot_index += subplot_columns


    if args.voltage:
      plt.subplot(subplot_rows, subplot_columns, plot_index)
      plt.plot(time[index], current[index], color=color)
      plt.xlabel('Time (s)', fontsize=20)
      plt.ylabel('Current (mA)', fontsize=20)
      plt.grid(True)
      plot_index += subplot_columns


    if not args.no_power:
      plt.subplot(subplot_rows, subplot_columns, plot_index)
      plt.plot(time[index], power[index], color=color)
      plt.xlabel('Time (s)', fontsize=20)
      plt.ylabel('Power (mW)', fontsize=20)
      plt.grid(True)
  plt.show()


def show_merged_plot(time, voltage, current, power, args):

  plt.suptitle(args.title, fontsize=26)
  plt.xlabel('Time (s)', fontsize=20)
  plt.ylabel('Power (mW)', fontsize=20)
  plt.grid(True)

  for index in range(0, len(args.input)):
    color_index = index if index < len(PLOT_COLORS) else 0
    color = PLOT_COLORS[color_index]

    plt.plot(time[index], power[index], color=color)
  plt.show()


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
  parser.add_argument('input', nargs='+', default=[],
                      help='Input CSV file(s) to process.')

  args = parser.parse_args()

  time, voltage, current, power = load_input_files(args.input)

  if not args.statistics:
    if args.merged:
      show_merged_plot(time, voltage, current, power, args)
    else:
      show_subplots(time, voltage, current, power, args, PLOT_COLORS.index('k'))

  else:
    for index in range(0, len(args.input)):
      t = time[index]

      print('Statistics for the input file: {}'.format(args.input[index]))
      print('  average:')
      print('    voltage: {:.3f} V'.format(mean(voltage[index])))
      print('    current: {:.3f} mA'.format(mean(current[index])))
      print('    power:   {:.3f} mW'.format(mean(power[index])))
      print('  measurement time: {}'.format(t[len(t) - 1 ] - t[0]))
      print()

  print('Done.')