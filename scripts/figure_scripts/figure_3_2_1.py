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
measurement_id = 'fibonacci_{}'.format(nterms)
# uncomment to take input from the user
#nterms = int(input("How many terms? "))

# first two terms
n1 = 0
n2 = 1
count = 0

send_message(Command.START, measurement_id)
time.sleep(1)

# check if the number of terms is valid
if nterms <= 0:
   print("Please enter a positive integer")
elif nterms == 1:
   print("Fibonacci sequence upto",nterms,":")
   print(n1)
else:
   print("Fibonacci sequence upto",nterms,":")
   while count < nterms:
       print(n1,end=' , ')
       nth = n1 + n2
       # update values
       n1 = n2
       n2 = nth
       count += 1

time.sleep(1)
send_message(Command.STOP, measurement_id)
