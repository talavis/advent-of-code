import requests

day = 18
part1 = True
part2 = True
testing = True
active = True

test_data = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

test_data2 = test_data

test_ans1 = 62
test_ans2 = 952408144115


def parse(indata):
    data_rows = indata.split("\n")
    data = [row.split() for row in data_rows if row]
    data = [[row[0], int(row[1]), row[2][2:-1]] for row in data]
    return data


def calc(data):
    dirs = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}
    C = dirs.values()

    def fill(start, blocks):
        queue = [start]
        blocks[start[0]][start[1]] = "X"
        while queue:
            c = queue.pop(0)
            for d in C:
                new_c = [c[0] + d[0], c[1] + d[1]]
                if blocks[new_c[0]][new_c[1]] == ".":
                    blocks[new_c[0]][new_c[1]] = "X"
                    queue.append(new_c)

    def normalise(ul, dug):
        x_change = 0 - ul[0]
        y_change = 0 - ul[1]
        for i in range(len(dug)):
            dug[i][0] += x_change
            dug[i][1] += y_change

    dug = [[0, 0]]
    pos = [0, 0]
    dirs = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}

    for inst in data:
        for _ in range(inst[1]):
            pos[0] += dirs[inst[0]][0]
            pos[1] += dirs[inst[0]][1]
            dug.append(list(pos))

    ul = [min([d[0] for d in dug]), min([d[1] for d in dug])]
    lr = [max([d[0] for d in dug]), max([d[1] for d in dug])]

    normalise(ul, dug)

    area = [["."] * (lr[1] - ul[1] + 1) for _ in range(lr[0] - ul[0] + 1)]

    for p in dug:
        area[p[0]][p[1]] = "#"

    for i in range(len(area[0])):
        if area[0][i] == ".":
            fill([0, i], area)
    for i in range(len(area[-1])):
        if area[-1][i] == ".":
            fill([-1, i], area)
    for i in range(len(area)):
        if area[i][0] == ".":
            fill([i, 0], area)
        if area[i][-1] == ".":
            fill([i, -1], area)

    score = 0
    for row in area:
        r = "".join(row)
        score += r.count("#") + r.count(".")

    return score


def calc2(data):
    def shoelace(vertices):
        num_vert = len(vertices)
        sum1 = 0
        sum2 = 0
        for i in range(0, num_vert - 1):
            sum1 = sum1 + vertices[i][0] * vertices[i + 1][1]
            sum2 = sum2 + vertices[i][1] * vertices[i + 1][0]
        sum1 = sum1 + vertices[-1][0] * vertices[0][1]
        sum2 = sum2 + vertices[0][0] * vertices[-1][1]

        area = abs(sum1 - sum2) / 2
        return area

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    inst = []
    for d in data:
        inst.append([int(d[2][:-1], 16), int(d[2][-1])])

    # pick's theorem, first time :o
    # calculate area of polygon with integer vertices
    # A = i + b/2 -1  # i: interior integer points, b: boundary integer points
    # i + b/2 = A + 1
    # score = i + b = A + 1 + b/2

    # b = length of dig
    b = sum(e[0] for e in inst)

    # shoelace formula: calculate area of polygon
    vertices = []
    pos = [0, 0]
    for e in inst:
        pos[0] += dirs[e[1]][0] * e[0]
        pos[1] += dirs[e[1]][1] * e[0]
        vertices.append(list(pos))

    vertices = vertices[::-1]  # anti-clockwise

    A = int(shoelace(vertices))
    # i + b/2 = A + 1
    # score = i + b
    score = A + 1 + b // 2

    return score


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
        raw = requests.get(f"https://adventofcode.com/2023/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
