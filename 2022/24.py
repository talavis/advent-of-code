import functools
import requests

day = 24
part1 = True
part2 = True
testing = True
active = True


def parse(indata):
    data_rows = indata.split("\n")
    return tuple(row for row in data_rows if row)


def calc_block_rate(data, blizz_steps):
    blocked = [[set() for _ in data[0]] for row in data]
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == "#":
                blocked[i][j] = set(range(len(blizz_steps)))
    for s, bstep in enumerate(blizz_steps):
        for b in bstep:
            blocked[b[0]][b[1]].add(s)
    return blocked


def blizz_dir(direction):
    if direction == ">":
        return (0, 1)
    elif direction == "<":
        return (0, -1)
    elif direction == "^":
        return (-1, 0)
    elif direction == "v":
        return (1, 0)


def step(positions, dirs, b_size):
    new_pos = []
    for i, pos in enumerate(positions):
        npos = [pos[0] + dirs[i][0], pos[1] + dirs[i][1]]
        if npos[0] == 0:
            npos[0] = b_size[0] - 2
        elif npos[0] == b_size[0] - 1:
            npos[0] = 1
        elif npos[1] == 0:
            npos[1] = b_size[1] - 2
        elif npos[1] == b_size[1] - 1:
            npos[1] = 1
        new_pos.append(npos)
    return tuple(new_pos)


@functools.cache
def precalc(data, cycle):
    b_size = (len(data), len(data[0]))
    blizz_dirs = []
    blizz_steps = [[]]
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c not in ("#", "."):
                blizz_steps[0].append((i, j))
                blizz_dirs.append(blizz_dir(c))

    for _ in range(cycle - 1):
        blizz_steps.append(step(blizz_steps[-1], blizz_dirs, b_size))

    return calc_block_rate(data, blizz_steps)


def common_div(val1, val2):
    i = 2
    divs = 1
    while i <= val1 or i <= val2:
        dived = False
        if val1 % i == 0:
            val1 //= i
            dived = True
        if val2 % i == 0:
            val2 //= i
            dived = True
        if dived:
            divs *= i
        else:
            i += 1
    return divs


def solve(start, target, blocked, cycle, s=0):
    current = {start}
    while target not in current:
        s += 1
        future = set()
        for pos in current:
            if pos[0] == 0:
                possible = [pos, (pos[0] + 1, pos[1])]
            elif pos[0] == len(blocked)-1:
                possible = [pos, (pos[0] - 1, pos[1])]
            else:
                possible = [
                    pos,
                    (pos[0] - 1, pos[1]),
                    (pos[0] + 1, pos[1]),
                    (pos[0], pos[1] - 1),
                    (pos[0], pos[1] + 1),
                ]
            for poss in possible:
                if (s + 1) % cycle not in blocked[poss[0]][poss[1]]:
                    future.add(poss)
        current = future
    return s


def calc(data):
    start = (0, data[0].index("."))
    pos = (0, data[0].index("."))
    target = (len(data) - 1, data[-1].index("."))
    cycle = common_div(len(data), len(data[0]))
    blocked = precalc(data, cycle)

    current = {start}
    s = solve(start, target, blocked, cycle)
    s += 1
    return s
            

def calc2(data):
    start = (0, data[0].index("."))
    pos = (0, data[0].index("."))
    target = (len(data) - 1, data[-1].index("."))
    cycle = common_div(len(data), len(data[0]))
    blocked = precalc(data, cycle)
    s = 0
    s = solve(start, target, blocked, cycle, s)
    s = solve(target, start, blocked, cycle, s)
    s = solve(start, target, blocked, cycle, s)
    s += 1

    return s


test_data = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

if testing:
    test_data = parse(test_data)

    if part1:
        res1 = calc(test_data)
        ans1 = 18
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    if part2:
        res2 = calc2(test_data)
        ans2 = 54
        print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

if active:
    cookies = {"session": open("cookie.dat").read()}
    try:
        raw = open(f"{day}.txt").read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    data = parse(raw)
    if part1:
        print(f"Part 1: {calc(data)}")
    if part2:
        print(f"Part 2: {calc2(data)}")
