import collections

import requests

day = 8
part1 = True
part2 = True
testing = True
active = True

test_data = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

test_data2 = test_data

test_ans1 = 14
test_ans2 = 34


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data):
    antennas = dict()
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c != ".":
                if c not in antennas:
                    antennas[c] = [(i, j)]
                else:
                    antennas[c].append((i, j))
    antinodes = set()
    for ant in antennas:
        ants = antennas[ant]
        for c in range(len(ants)):
            for d in range(c + 1, len(ants)):
                a = ants[c]
                b = ants[d]
                # a[0] is alsways <= b[0]
                x_change = b[0] - a[0]
                if a[1] <= b[1]:
                    y_change = b[1] - a[1]
                    pot_anti = (a[0] - x_change, a[1] - y_change)
                    if 0 <= pot_anti[0] < len(data) and 0 <= pot_anti[1] < len(data[0]):
                        antinodes.add(pot_anti)
                    pot_anti = (b[0] + x_change, b[1] + y_change)
                    if 0 <= pot_anti[0] < len(data) and 0 <= pot_anti[1] < len(data[0]):
                        antinodes.add(pot_anti)
                if a[1] > b[1]:
                    y_change = a[1] - b[1]
                    pot_anti = (a[0] - x_change, a[1] + y_change)
                    if 0 <= pot_anti[0] < len(data) and 0 <= pot_anti[1] < len(data[0]):
                        antinodes.add(pot_anti)
                    pot_anti = (b[0] + x_change, b[1] - y_change)
                    if 0 <= pot_anti[0] < len(data) and 0 <= pot_anti[1] < len(data[0]):
                        antinodes.add(pot_anti)
    return len(antinodes)


def calc2(data):
    antennas = dict()
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c != ".":
                if c not in antennas:
                    antennas[c] = [(i, j)]
                else:
                    antennas[c].append((i, j))
    antinodes = set()
    for ant in antennas:
        ants = antennas[ant]
        for c in range(len(ants)):
            for d in range(c + 1, len(ants)):
                a = ants[c]
                b = ants[d]
                dx = a[0] - b[0]
                dy = a[1] - b[1]
                while 0 <= a[0] < len(data) and 0 <= a[1] < len(data[0]):
                    antinodes.add(a)
                    a = (a[0] - dx, a[1] - dy)
                while 0 <= b[0] < len(data) and 0 <= b[1] < len(data[0]):
                    antinodes.add(b)
                    b = (b[0] + dx, b[1] + dy)
    return len(antinodes)


if testing:
    if part1:
        test_data_p = parse(test_data)
        res1 = calc(test_data_p)
        ans1 = test_ans1
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")

    if part2:
        test_data_p2 = parse(test_data2)
        res2 = calc2(test_data_p2)
        ans2 = test_ans2
        print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

if active:
    cookies = {"session": open("cookie.dat").read()}
    try:
        raw = open(f"{day}.txt").read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2024/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
