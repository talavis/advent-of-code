#!/usr/bin/env python3

import sys

inputs = tuple(int(i) for i in open(sys.argv[1]).read().split('\n') if i)

value = 0
saved = set()

i = 0
while value not in saved:
    saved.add(value)
    value += inputs[i]
    
    i += 1
    if i == len(inputs):
        i = 0
    
print(value)
