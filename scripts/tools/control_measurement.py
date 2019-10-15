#!/usr/bin/env python3

import os
import sys
import argparse

sys.path.append('../')

from communication_helpers.communication_helper import Command, send_message

if __name__ == '__main__':
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('command', choices=['start', 'stop'],
                      help='Start / stop the energy measurement.')
  parser.add_argument('message',
                      help='Start / stop the measurement with the given message.')

  args = parser.parse_args()

  command = Command.START if args.command == 'start' else Command.STOP
  send_message(command, args.message)
