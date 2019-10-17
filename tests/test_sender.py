#!/usr/bin/env python3

import os
import sys
import time

from scripts.communication_helpers.communication_helper import Command, send_message

send_message(Command.START, 'test_sender.py:27')
time.sleep(4)
send_message(Command.STOP, 'test_sender.py:27')

send_message(Command.START, 'test_sender.py:28')
time.sleep(2)
send_message(Command.STOP, 'test_sender.py:28')
