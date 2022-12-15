#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as infile:
    values = [int(val) for val in infile.read().strip().split(',')]
    values[1] = 12
    values[2] = 2
    for i in range(0, len(values), 4):
        if values[i] == 1:
            values[values[i+3]] = values[values[i+1]] + values[values[i+2]]
        elif values[i] == 2:
            values[values[i+3]] = values[values[i+1]] * values[values[i+2]]
        elif values[i] == 99:
            break

print(f'Part a: {values[0]}')

with open(sys.argv[1]) as infile:
    VALUES = [int(val) for val in infile.read().strip().split(',')]

for noun in range(0, 100):
    for verb in range(0, 100):
        values = VALUES[:]
        values[1] = noun
        values[2] = verb
        try:
            for i in range(0, len(values), 4):
                if values[i] == 1:
                    values[values[i+3]] = values[values[i+1]] + values[values[i+2]]
                elif values[i] == 2:
                    values[values[i+3]] = values[values[i+1]] * values[values[i+2]]
                elif values[i] == 99:
                    break
        except IndexError:
            continue
        if values[0] == 19690720:
            print(f'Part b: {100*noun+verb}')
            sys.exit(0)
sys.exit(1)
