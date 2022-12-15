#!/usr/bin/env python3

import logging
import sys


#logging.basicConfig(level=logging.DEBUG)

def get_params(values, modes, i, nr_params):
    params = []
    for j in range(nr_params):
        if j >= len(modes) or modes[j] == 0:
            params.append(values[values[i+1+j]])
        elif modes[j] == 1:
            params.append(values[i+1+j])
        else:
            sys.stderr.write(f'Bad mode: {modes[j]}')
    return params


def run_machine(values, input_values=[1]):
    input_i = 0
    i = 0
    outputs = []
    while values[i] != 99 and i < len(values):
        logging.debug(f'Values: {[v if ind !=i else f"_{v}_ "for ind, v in enumerate(values)]}, i={i}')
        val, modes = get_modes(values[i])
        logging.debug(f'operation: {val}, modes: {modes}')
        if val == 1:
            params = get_params(values, modes, i, 2)
            logging.debug(f'params: {params}')
            values[values[i+3]] = params[0] + params[1]
            logging.debug(f'values[{values[i+3]}] = {params[0]} + {params[1]}')
            i += 4
        elif val == 2:
            params = get_params(values, modes, i, 2)
            logging.debug(f'params: {params}')
            values[values[i+3]] = params[0] * params[1]
            logging.debug(f'values[{values[i+3]}] = {params[0]} * {params[1]}')
            i += 4
        elif val == 3:
            values[values[i+1]] = input_values[input_i]
            logging.debug(f'values[{values[i+1]}] = {input_values[input_i]}')
            input_i += 1
            i += 2
        elif val == 4:
            params = get_params(values, modes, i, 1)
            outputs.append(params[0])
            logging.debug(f'out: {params[0]}')
            if params[0] != 0:
                logging.error('Bad code')
            i += 2
        elif val == 5:
            params = get_params(values, modes, i, 2)
            if params[0] != 0:
                logging.debug(f'Non-zero, i={params[1]}')
                i = params[1]
            else:
                i += 3
        elif val == 6:
            params = get_params(values, modes, i, 2)
            if params[0] == 0:
                logging.debug(f'Zero, i={params[1]}')
                i = params[1]
            else:
                i += 3
        elif val == 7:
            params = get_params(values, modes, i, 2)
            logging.debug(f'Less-than test')
            if params[0] < params[1]:
                values[values[i+3]] = 1
            else:
                values[values[i+3]] = 0
            i += 4
        elif val == 8:
            logging.debug(f'equal test')
            params = get_params(values, modes, i, 2)
            if params[0] == params[1]:
                values[values[i+3]] = 1
            else:
                values[values[i+3]] = 0
            i += 4
        else:
            logging.error('Bad operation')
    return outputs


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

if __name__ == '__main__':
    with open(sys.argv[1]) as infile:
        VALUES = [int(val) for val in infile.read().strip().split(',')]

    values = VALUES[:]
    outputs = run_machine(values, input_values=[1])
    print(f'Part a: {outputs[-1]}')

    values = VALUES[:]
    outputs = run_machine(values, input_values=[5])
    print(f'Part b: {outputs[-1]}')
