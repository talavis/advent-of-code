#!/usr/bin/env python3

import sys

value = 0

for line in open(sys.argv[1]):
    value += int(line)
    

print(value)
