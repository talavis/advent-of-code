import collections

import requests

day = 6
part1 = True
part2 = True
testing = True
active = True

test_data = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

test_data2 = test_data

test_ans1 = 41
test_ans2 = 6


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data):
    for i, row in enumerate(data):
        if "^" in row:
            pos = (i, row.index("^"))

    visited = {pos}
    dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
    d = 0

    while True:
        new_pos = (pos[0] + dirs[d][0], pos[1] + dirs[d][1])
        if (
            new_pos[0] < 0
            or new_pos[0] == len(data)
            or new_pos[1] < 0
            or new_pos[1] == len(data[0])
        ):
            break
        if data[new_pos[0]][new_pos[1]] == "#":
            d = (d + 1) % 4
            continue
        pos = new_pos
        visited.add(pos)

    return len(visited)


def calc2(data):
    for i, row in enumerate(data):
        if "^" in row:
            pos = (i, row.index("^"))
    POS = pos

    visited = {pos}
    dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
    d = 0

    while True:
        new_pos = (pos[0] + dirs[d][0], pos[1] + dirs[d][1])
        if (
            new_pos[0] < 0
            or new_pos[0] == len(data)
            or new_pos[1] < 0
            or new_pos[1] == len(data[0])
        ):
            break
        if data[new_pos[0]][new_pos[1]] == "#":
            d = (d + 1) % 4
            continue
        pos = new_pos
        visited.add(pos)

    loops = 0
    for o in visited:
        if o == POS:
            continue
        moves = set()
        pos = POS
        d = 0
        while True:
            new_pos = (pos[0] + dirs[d][0], pos[1] + dirs[d][1])
            if (
                new_pos[0] < 0
                or new_pos[0] == len(data)
                or new_pos[1] < 0
                or new_pos[1] == len(data[0])
            ):
                break
            if data[new_pos[0]][new_pos[1]] == "#" or new_pos == o:
                d = (d + 1) % 4
                continue
            if (pos, new_pos) in moves:
                loops += 1
                break
            moves.add((pos, new_pos))
            pos = new_pos
    return loops


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
