#!/usr/bin/env python3


import sys

def parse_input(rawtext):
    lines = rawtext.split('\n')
    plants = lines[0][15:]
    plants = plants.replace('.', '0')
    plants = plants.replace('#', '1')
    plants = tuple(int(val) for val in plants)

    cases = dict()
    for line in lines[2:]:
        if line:
            line = line.replace('.', '0')
            line = line.replace('#', '1')
            cases[tuple(int(val) for val in line[:5])] = int(line[9])
    return plants, cases


def plantstep(plants, cases, modifier=0):
    left = []
    if plants[:4] != [0]*4:
        inc = len(plants)//8
        left += [0]*inc
        modifier -= inc
    right = []
    if plants[-4:] != [0]*4:
        right = [0]*4
    new_plants = left+list(plants)+right
    plants = tuple(new_plants)

    for i in range(plants.index(1)-3, len(plants)-1):
        present = plants[i-2:i+3]

        if present in cases:
            new_plants[i] = cases[present]
        else:
            new_plants[i] = 0
    return new_plants, modifier


def potsum(plants, modifier):
    sum_pots = 0
    for i in range(len(plants)):
        if plants[i]:
            sum_pots += i+modifier
    return sum_pots


def plants_to_str(plants):
    txt = ''.join([str(val) for val in plants])
    txt = txt.replace('0', '.')
    txt = txt.replace('1', '#')
    return txt


def test_plantstep():
    rawtext = '''initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #'''

    plants, cases = parse_input(rawtext)

    assert plants_to_str(plants) == '#..#.#..##......###...###'
    plants, modifier = plantstep(plants, cases)
    assert plants_to_str(plants).strip('.') == '#...#....#.....#..#..#..#'
    for i in range(19):
        plants, modifier = plantstep(plants, cases, modifier)
    assert plants_to_str(plants).strip('.') == '#....##....#####...#######....#.#..##'

    assert potsum(plants, modifier) == 325


def main():
    rawtext = open(sys.argv[1]).read()
    plants, cases = parse_input(rawtext)
    modifier = 0
    # observation: increase seems to stabilise after a while
    diff = 0
    oldsum = 0
    for i in range(20000):
        plants, modifier = plantstep(plants, cases, modifier)
        newsum = potsum(plants, modifier)
        if newsum-oldsum == diff:
            print(newsum+diff*(50000000000-i-1))
            break
        diff = newsum-oldsum
        oldsum = newsum


if __name__ == '__main__':
    main()
