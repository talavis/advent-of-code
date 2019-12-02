#!/usr/bin/env python3

import sys

def calc_fuel(mass):
    fuel = int(mass/3)
    fuel -= 2
    if fuel < 0:
        fuel = 0
    return fuel


with open(sys.argv[1]) as infile:
    fuel_sum = 0
    for line in infile:
        mass = int(line)
        fuel_sum += calc_fuel(mass)
print(f'Part a: {fuel_sum}')


with open(sys.argv[1]) as infile:
    fuel_sum = 0
    for line in infile:
        mass = int(line)
        new_fuel = mass
        while new_fuel > 0:
            new_fuel = calc_fuel(new_fuel)
            fuel_sum += new_fuel

print(f'Part b: {fuel_sum}')
