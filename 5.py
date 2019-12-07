#!/usr/bin/env python3

import logging
import sys


logging.basicConfig(level=logging.DEBUG)

def run_machine(values, input_values=[1], prefix='Output'):
    input_i = 0
    i = 0
    while values[i] != 99:
        logging.debug(i)
        logging.debug(f'range: {values[i:i+4]}')
        val, modes = get_modes(values[i])
        logging.debug(f'{val}, {modes}')
        if val == 1:
            params = []
            for j in range(2):
                if j >= len(modes) or modes[j] == 0:
                    params.append(values[values[i+1+j]])
                elif modes[j] == 1:
                    params.append(values[i+1+j])
                else:
                    sys.stderr.write(f'Bad mode: {modes[j]}')
            logging.debug(f'params: {params}')
            values[values[i+3]] = params[0] + params[1]
            i += 4
        elif val == 2:
            params = []
            for j in range(3):
                if j >= len(modes) or modes[j] == 0:
                    params.append(values[values[i+1+j]])
                elif modes[j] == 1:
                    params.append(values[i+1+j])
                else:
                    sys.stderr.write(f'Bad mode: {modes[j]}')
            logging.debug(params)
            values[values[i+3]] = params[0] * params[1]
            i += 4
        elif val == 3:
            values[values[i+1]] = input_values[input_i]
            input_i += 1
            i += 2
        elif val == 4:
            print(f'{prefix}: {values[values[i+1]]}')
            i += 2


def get_modes(value):
    logging.debug(f'value (modes): {value}')
    if value < 100:
        return value, []
    val = value % 100
    value //= 100
    modes = []
    while value > 0:
        modes.append(value%10)
        value //= 10
    return val, modes


with open(sys.argv[1]) as infile:
    values = [int(val) for val in infile.read().strip().split(',')]
    run_machine(values, input_values=[1], prefix='Part a')
