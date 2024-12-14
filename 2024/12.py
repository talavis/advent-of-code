import requests

day = 12
part1 = True
part2 = True
testing = True
active = True

test_data = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

test_data2 = test_data

test_ans1 = 1930
test_ans2 = 1206


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data):
    regions = []
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for i in range(len(data)):
        for j in range(len(data[i])):
            new_reg = True
            for reg in regions:
                if (i, j) in reg:
                    new_reg = False
                    break
            if new_reg:
                regions.append(set())
                val = data[i][j]
                stack = {(i, j)}
                while stack:
                    pos = stack.pop()
                    regions[-1].add(pos)
                    for d in dirs:
                        new_pos = (pos[0] + d[0], pos[1] + d[1])
                        if (
                            new_pos not in regions[-1]
                            and 0 <= new_pos[0] < len(data)
                            and 0 <= new_pos[1] < len(data[0])
                            and data[new_pos[0]][new_pos[1]] == val
                        ):
                            stack.add(new_pos)

    ans = 0
    for reg in regions:
        peri = 0
        for pos in reg:
            for d in dirs:
                n = (pos[0] + d[0], pos[1] + d[1])
                if n not in reg:
                    peri += 1
        ans += peri * len(reg)
    return ans


def calc2(data):
    regions = []
    dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
    for i in range(len(data)):
        for j in range(len(data[i])):
            new_reg = True
            for reg in regions:
                if (i, j) in reg:
                    new_reg = False
                    break
            if new_reg:
                regions.append(set())
                val = data[i][j]
                stack = {(i, j)}
                while stack:
                    pos = stack.pop()
                    regions[-1].add(pos)
                    for d in dirs:
                        new_pos = (pos[0] + d[0], pos[1] + d[1])
                        if (
                            new_pos not in regions[-1]
                            and 0 <= new_pos[0] < len(data)
                            and 0 <= new_pos[1] < len(data[0])
                            and data[new_pos[0]][new_pos[1]] == val
                        ):
                            stack.add(new_pos)

    ans = 0
    for reg in regions:
        # n_edges == corners
        corners = 0
        dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))
        corner_pos = ((0, 1), (1, 2), (2, 3), (3, 0))
        diagonals = ((1, 1), (-1, 1), (-1, -1), (1, -1))
        for pos in reg:
            neighbours = []
            for d in dirs:
                neighbours.append((pos[0] + d[0], pos[1] + d[1]))
            for c in corner_pos:
                # "external" corners (two sides empty)
                if neighbours[c[0]] not in reg and neighbours[c[1]] not in reg:
                    corners += 1
                # "internal corners" (all sides exist, but neighbours have missing corrsesponding neighbours)
                if neighbours[c[0]] in reg and neighbours[c[1]] in reg:
                    if (
                        pos[0] + diagonals[c[0]][0],
                        pos[1] + diagonals[c[0]][1],
                    ) not in reg:
                        corners += 1
        ans += corners * len(reg)
    return ans


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
