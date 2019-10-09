#!/usr/bin/env python3

# Source: https://www.programiz.com/python-programming/examples/fibonacci-sequence
# Program to display the Fibonacci sequence up to n-th term where n is provided by the user

import os
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('../')

from communication_helper import Command, send_message

# change this value for a different result
nterms = 10000

# first two terms
n1 = 0
n2 = 1
count = 0

send_message(Command.START, 'fibonacci')
time.sleep(1)

fibonacci_sequence = [ n2 ]

while count < nterms:
    nth = n1 + n2
    fibonacci_sequence.append(nth)

    # update values
    n1 = n2
    n2 = nth
    count += 1

time.sleep(1)

with open('fibonacci_sequence.txt', 'w') as f:
    for item in fibonacci_sequence:
        f.write('{}, '.format(item))

time.sleep(1)
send_message(Command.STOP, 'fibonacci')
