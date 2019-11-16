#!/usr/bin/env python3

# Source: https://www.programiz.com/python-programming/examples/fibonacci-sequence
# Program to display the Fibonacci sequence up to n-th term where n is provided by the user

import os
import sys
import time

from scripts.communication_helpers.communication_helper import Command, send_message

# change this value for a different result
nterms = 100000

# first two terms
n1 = 0
n2 = 1
count = 0

send_message(Command.START, 'fibonacci')

fibonacci_sequence = [ n2 ]

while count < nterms:
    nth = n1 + n2
    fibonacci_sequence.append(nth)

    # update values
    n1 = n2
    n2 = nth
    count += 1

print ('Calculation done.')
with open('fibonacci_sequence.txt', 'w') as f:
    max_index = len(fibonacci_sequence) if len(fibonacci_sequence) < 15000 else 15000

    for index in range(max_index):
        f.write('{},'.format(fibonacci_sequence[index]))

send_message(Command.STOP, 'fibonacci')
