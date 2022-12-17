import requests

day = 17

SHAPES = [
    ["####"],
    [".#.", "###", ".#."],
    ["..#", "..#", "###"],
    ["#", "#", "#", "#"],
    ["##", "##"],
]

def new_rock(s):
    shape = SHAPES[s]
    s += 1
    if s >= len(SHAPES):
        s = 0
    return s, shape


def extend_matrix(matrix, rock):
    i = -1
    while -i <= len(matrix):
        if "#" in matrix[i]:
            break
        i -= 1

    for j in range(4 + i + len(rock)):
        print("extend")
        matrix.append(["."] * 7)


def check_collision(rock, matrix, x, y):
    if x + len(rock[0]) > 7 or x < 0:  # wind movement
        return True
    if y - len(rock) + 1 < 0:  # hit the bottom
        return True
    for i, row in enumerate(rock):
        for j, char in enumerate(row):
            if char == "#" and matrix[y - i][x + j] == "#":
                return True
    return False


def find_start(rock, matrix):
    for i in range(len(matrix)):
        if "#" not in matrix[i]:
            break
    return i + 2 + len(rock)


def rock_to_matrix(rock, matrix, x, y):
    for i, row in enumerate(rock):
        for j, char in enumerate(row):
            if char == "#":
                matrix[y - i][x + j] = char


def calc(data):
    wind = [int(val == ">") or -1 for val in data]
    score = 0
    total = 0
    s = 0  # shape
    w = 0  # wind
    matrix = [["."] * 7 for _ in range(8000)]
    rock = None
    x = 2
    y = -1
    while total < 2022:  # steps
        if not rock:
            s, rock = new_rock(s)
            y = find_start(rock, matrix)
            x = 2
            # wind
            if not check_collision(rock, matrix, x + wind[w], y):
                x += wind[w]
            w += 1
            if w >= len(wind):
                w = 0
            continue
        # fall
        if not check_collision(rock, matrix, x, y - 1):
            y -= 1
        else:
            rock_to_matrix(rock, matrix, x, y)
            rock = None
            total += 1
            continue
        # wind
        if not check_collision(rock, matrix, x + wind[w], y):
            x += wind[w]
        w += 1
        if w >= len(wind):
            w = 0
    for i in range(-1, -len(matrix), -1):
        if "#" in matrix[i]:
            break
    return len(matrix) + i + 1


def calc2(data):
    wind = [int(val == ">") or -1 for val in data]
    score = 0
    total = 0
    s = 0  # shape
    w = 0  # wind
    matrix = [["."] * 7 for _ in range(100_000)]
    rock = None
    x = 2
    y = -1
    tops = {}
    lh = 0
    diff = 140  #  1926
    cycle = 1730
    heights = []
    while total < 10_000:  # steps
        if not rock:
            s, rock = new_rock(s)
            y = find_start(rock, matrix)
            row = "".join(matrix[y - 3 - len(rock)])
            heights.append(y - 2 - len(rock))
            if row not in tops:
                tops[row] = [total]
            else:
                tops[row].append(total)
            x = 2
            # wind
            if not check_collision(rock, matrix, x + wind[w], y):
                x += wind[w]
            w += 1
            if w >= len(wind):
                w = 0
            continue
        # fall
        if not check_collision(rock, matrix, x, y - 1):
            y -= 1
        else:
            rock_to_matrix(rock, matrix, x, y)
            rock = None
            total += 1
            continue
        # wind
        if not check_collision(rock, matrix, x + wind[w], y):
            x += wind[w]
        w += 1
        if w >= len(wind):
            w = 0

    # analyse
    gaps = {}
    gap_example = {}
    for entry in tops:
        start = len(tops[entry]) - 10
        if start < 0:
            start = 0
        for i in range(start, len(tops[entry])):
            gap = tops[entry][i] - tops[entry][i - 1]
            if gap in gaps:
                gaps[gap] += 1
            else:
                gaps[gap] = 0
            gap_example[gap] = tops[entry][i]

    cycle = sorted(gaps.items(), key=lambda x: x[1])[-1][0]
    goal = 1000000000000
    diff = goal % cycle
    i = (len(heights) // cycle - 1) * cycle + diff
    change = heights[i] - heights[i - cycle]
    val = heights[i] + change * (goal // cycle - i // cycle)
    return val


test_data = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

testing = True
if testing:
    res1 = calc(test_data)
    res2 = calc2(test_data)
    ans1 = 3068
    ans2 = 1514285714288
    print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

active = True
if active:
    cookies = {"session": open("cookie.dat").read()}
    req = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies).text
    # req =  open(f"{day}.txt").read()
    data = req

    print(f"Part 1: {calc(data)}")
    print(f"Part 2: {calc2(data)}")
