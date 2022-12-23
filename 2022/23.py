import requests

day = 23
part1 = True
part2 = True
testing = True
active = True


def parse(indata):
    data_rows = indata.split("\n")
    data = [list(row) for row in data_rows if row]
    return data


DIRS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


def find_nearby(elf, elves):
    nearby = set()
    for d in DIRS:
        tmp = (elf[0] + d[0], elf[1] + d[1])
        if tmp in elves:
            nearby.add(tmp)
    return nearby


def draw(elves):
    y = [e[0] for e in elves]
    x = [e[1] for e in elves]
    for i in range(min(y), max(y) + 1):
        out = list("." * (max(x) - min(x) + 1))
        for e in elves:
            if e[0] == i:
                out[e[1] - min(x)] = "#"
        print("".join(out))
    print()


def north(elf, x, y):
    if not elf[0] - 1 in y:
        return (elf[0] - 1, elf[1])


def south(elf, x, y):
    if not elf[0] + 1 in y:
        return (elf[0] + 1, elf[1])


def west(elf, x, y):
    if not elf[1] - 1 in x:
        return (elf[0], elf[1] - 1)


def east(elf, x, y):
    if not elf[1] + 1 in x:
        return (elf[0], elf[1] + 1)


def step(elves, decisions):
    suggestions = []
    elves_s = set(elves)
    for elf in elves:
        nearby = find_nearby(elf, elves_s)
        y = [e[0] for e in nearby]
        x = [e[1] for e in nearby]
        inc = None
        if nearby:
            for d in decisions:
                res = d(elf, x, y)
                if res:
                    inc = res
                    break
        if not inc:
            inc = elf
        suggestions.append(inc)

    changed = True
    sugs = suggestions
    new_elves = []
    for i, sug in enumerate(sugs):
        if sugs.count(sug) > 1:
            new_elves.append(elves[i])
        else:
            new_elves.append(sug)
    return new_elves


def calc(data):
    elves = []
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == "#":
                elves.append((i, j))

    decisions = [north, south, west, east]
    for _ in range(10):
        elves = step(elves, decisions)
        decisions = decisions[1:] + [decisions[0]]
    limits = [0] * 4
    y = [e[0] for e in elves]
    x = [e[1] for e in elves]
    limits[0] = min(y)
    limits[1] = max(y)
    limits[2] = min(x)
    limits[3] = max(x)

    return (limits[1] - limits[0] + 1) * (limits[3] - limits[2] + 1) - len(elves)


def calc2(data):
    elves = []
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == "#":
                elves.append((i, j))

    decisions = [north, south, west, east]
    moved = True
    i = 0
    while moved:
        new_elves = step(elves, decisions)
        decisions = decisions[1:] + [decisions[0]]
        moved = new_elves != elves
        elves = new_elves
        i += 1
        print(i)
    limits = [0] * 4
    y = [e[0] for e in elves]
    x = [e[1] for e in elves]
    limits[0] = min(y)
    limits[1] = max(y)
    limits[2] = min(x)
    limits[3] = max(x)
    return i


test_data1 = """.....
..##.
..#..
.....
..##.
....."""

test_data = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

if testing:
    test_data1 = parse(test_data1)
    test_data = parse(test_data)

    if part1:
        res1a = calc(test_data1)
        ans1a = 25
        print(f"Test part 1a: {res1a} ({ans1a}){'   !!!' if res1a != ans1a else ''}")
        res1 = calc(test_data)
        ans1 = 110
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    if part2:
        res2 = calc2(test_data)
        ans2 = 20
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
