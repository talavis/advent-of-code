#!/usr/bin/env python3


import sys

def parse_input(rawtext):
    lines = rawtext.split('\n')
    plants = list(lines[0][15:])
    cases = dict()
    for line in lines[2:]:
        if line:
            cases[line[:5]] = line[9]
    return plants, cases


def plantstep(plants, cases, modifier=0):
    new_plants = []
    if plants[:4] != '....':
        new_plants += list('....')
        plants = list('....') + plants
        modifier -= 4
    new_plants += plants
    if plants[-4:] != '....':
        new_plants += list('....')
        plants += list('....')

    for i in range(len(new_plants)):
        if i-2 < 0:
            present = ['.']*(2-i)
            present += plants[:i+3]
        elif i+2 >= len(plants):
            present += plants[i:]
            present = ['.']*(2-(len(plants)-i))
        else:
            present = plants[i-2:i+3]

        if ''.join(present) in cases:
            new_plants[i] = cases[''.join(present)]
        else:
            new_plants[i] = '.'
    return new_plants, modifier


def potsum(plants, modifier):
    potsum = 0
    for i in range(len(plants)):
        if plants[i] == '#':
            potsum += i+modifier
    return potsum


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
    assert ''.join(plants) == '#..#.#..##......###...###'
    plants, modifier = plantstep(plants, cases)
    assert ''.join(plants).strip('.') == '#...#....#.....#..#..#..#'
    for i in range(19):
        plants, modifier = plantstep(plants, cases, modifier)
    assert ''.join(plants).strip('.') == '#....##....#####...#######....#.#..##'

    assert potsum(plants, modifier) == 325


def main():
    rawtext = open(sys.argv[1]).read()
    plants, cases = parse_input(rawtext)
    modifier = 0
    for i in range(20):
        plants, modifier = plantstep(plants, cases, modifier)
    print(potsum(plants, modifier))

if __name__ == '__main__':
    main()
