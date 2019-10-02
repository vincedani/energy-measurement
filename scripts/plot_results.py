#!/usr/bin/env python3

import csv
import random
import datetime
import argparse
import matplotlib.pyplot as plt

PLOT_COLORS = ['b', 'g', 'r', 'c', 'm', 'k', 'w' ]

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


if __name__ == '__main__':
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('-c', '--current', action='store_true', default=False,
                      help='Show current values from the given CSV(s) on a subplot')
  parser.add_argument('-u', '--voltage', action='store_true', default=False,
                      help='Show voltage values from the given CSV(s) on a subplot')
  parser.add_argument('--no-power', action='store_true', default=False,
                      help='Do not show power values from the given CSV(s) on a subplot')
  parser.add_argument('input', nargs='+', default=[],
                      help='Input CSV file(s) to process.')
  parser.add_argument('--title', default='Untitled',
                      help='The title of the generated plot.')

  args = parser.parse_args()

  time, voltage, current, power = load_input_files(args.input)
  subplot_columns = len(args.input)
  subplot_rows = args.current + args.voltage + (not args.no_power)
  plot_index = 0

  plt.suptitle(args.title)
  for index in range(0, subplot_columns):
    current_plot_row = 1
    plot_index = index + 1

    color_index = 5 # black
    if subplot_columns > 1:
      color_index = random.randrange(0, len(PLOT_COLORS))

    t = time[index]
    u = voltage[index]
    i = current[index]
    p = power[index]

    if args.current:
      plt.subplot(subplot_rows, subplot_columns, plot_index)
      plt.plot(t, u, color=PLOT_COLORS[color_index])
      plt.xlabel('Time (s)')
      plt.ylabel('Voltage (V)')
      plt.grid(True)
      plot_index += subplot_columns


    if args.voltage:
      plt.subplot(subplot_rows, subplot_columns, plot_index)
      plt.plot(t, i, color=PLOT_COLORS[color_index])
      plt.xlabel('Time (s)')
      plt.ylabel('Current (mA)')
      plt.grid(True)
      plot_index += subplot_columns


    if not args.no_power:
      plt.subplot(subplot_rows, subplot_columns, plot_index)
      plt.plot(t, p, color=PLOT_COLORS[color_index])
      plt.xlabel('Time (s)')
      plt.ylabel('Power (mW)')
      plt.grid(True)
  plt.show()
