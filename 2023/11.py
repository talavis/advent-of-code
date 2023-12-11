import requests

day = 11
part1 = True
part2 = True
testing = False
active = True

test_data = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

test_ans1 = 374
test_ans2 = 8410


def parse(indata):
    data_rows = indata.split("\n")
    data = [list(row) for row in data_rows if row]
    return data


def calc(data):
    i = 0
    while i < len(data):
        if "#" not in data[i]:
            data.insert(i, ["."]*len(data[i]))
            i += 2
        i += 1

    cols = set(range(len(data[0])))
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == "#" and j in cols:
                cols.remove(j)

    cols = sorted(list(cols), reverse=True)
    for i in range(len(data)):
        for j in cols:
            data[i].insert(j, ".")

    galaxies = []
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == "#":
                galaxies.append((i, j))

    score = 0
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            score += abs(galaxies[i][0]-galaxies[j][0]) + abs(galaxies[i][1]-galaxies[j][1])
    return score


def calc2(data):
    # should be 10**3-1 for test 2
    multi = 10**6-1
    i = 0
    exp_r = set()
    exp_c = set()
    while i < len(data):
        if "#" not in data[i]:
            exp_r.add(i)
        i += 1

    exp_c = set(range(len(data[0])))
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == "#" and j in exp_c:
                exp_c.remove(j)

    galaxies = []
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == "#":
                galaxies.append((i, j))

    score = 0
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            dist = abs(galaxies[i][0]-galaxies[j][0]) + abs(galaxies[i][1]-galaxies[j][1])
            ri = sorted((galaxies[i][0], galaxies[j][0]))
            ci = sorted((galaxies[i][1], galaxies[j][1]))
            for r in exp_r:
                if ri[0] < r < ri[1]:
                    dist += multi
            for c in exp_c:
                if ci[0] < c < ci[1]:
                    dist += multi
            score += dist
    return score


if testing:
    test_data_p = parse(test_data)
    test_data_p2 = parse(test_data)

    if part1:
        res1 = calc(test_data_p)
        ans1 = test_ans1
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    if part2:
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
    data = parse(raw)
    data2 = parse(raw)
    if part1:
        print(f"Part 1: {calc(data)}")
    if part2:
        print(f"Part 2: {calc2(data2)}")
