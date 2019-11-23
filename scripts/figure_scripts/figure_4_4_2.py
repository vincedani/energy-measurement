#!/usr/bin/env python3

# Source: https://www.programiz.com/python-programming/examples/fibonacci-sequence
# Program to display the Fibonacci sequence up to n-th term where n is provided by the user

import os
import sys
import time

from scripts.communication_helpers.communication_helper import Command, send_message

def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j] :
                arr[j + 1] = arr[j]
                j -= 1
        arr[j + 1] = key

    return arr

nterms = int(sys.argv[1])
# first two terms
n1 = 0
n2 = 1
count = 0

send_message(Command.START, 'fibonacci_alg_python')

fibonacci_sequence = [ n2 ]

while count < nterms:
    nth = n1 + n2
    fibonacci_sequence.append(nth)

    # update values
    n1 = n2
    n2 = nth
    count += 1

fibonacci_sequence.reverse()
sorted_list = insertionSort(fibonacci_sequence)

with open('fibonacci_sequence_python.txt', 'w') as f:
    max_index = len(sorted_list) if len(sorted_list) < 15000 else 15000

    for index in range(max_index):
        f.write('{},'.format(sorted_list[index]))

send_message(Command.STOP, 'fibonacci_alg_python')
