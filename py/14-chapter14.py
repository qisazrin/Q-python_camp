# Module and libraries

# Module
# a file containing code (function, classes, variables,etc) that can be imported and used in other python programs.

# libraries
# a collection of module and packages that provide specific functionality

# module
# 1. create math_utils.py
# 2. import functions or class from math_utils.py

from math_utils import add, multiply, factorial, PI, calculator

result = add(5, 3)
print(f"Addition result: {result}")

# Libraries
import os
import sys
import datetime
import random


now = datetime.datetime.now()
today = datetime.date.today()
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

print()