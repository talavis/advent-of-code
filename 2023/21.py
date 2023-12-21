import collections

import requests

day = 21
part1 = True
part2 = True
testing = True
active = True

test_data = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

test_ans1 = 16


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data, steps=64):
    for i, row in enumerate(data):
        if "S" in row:
            start = (i, row.index("S"))
            break

    pos = {start}
    dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))  # urdl
    for i in range(steps):
        new_pos = set()
        for p in pos:
            for d in dirs:
                n = (p[0] + d[0], p[1] + d[1])
                if -len(data) <= n[0] < len(data) and 0 <= n[1] < len(data[0]):
                    if data[n[0] % len(data)][n[1] % len(data[0])] != "#":
                        new_pos.add(n)
        pos = new_pos

    return len(pos)


def calc2(data, steps=26501365):
    def find_neighbours(field):
        width = len(field[0])
        height = len(field[1])
        neighbours = {}
        dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))  # urdl

        for i, row in enumerate(field):
            for j, p in enumerate(row):
                if p == ".":
                    ns = []
                    for d in dirs:
                        di = i + d[0]
                        dj = j + d[1]
                        if 0 <= di < width and 0 <= dj < height and field[di][dj] == ".":
                            ns.append((di, dj))
                    neighbours[(i, j)] = ns
        return neighbours

    def calculate_fields(neighbours, width, height, start, steps):
        # calculate the possible squares
        positions = {(start, 0, 0)}
        for i in range(steps):
            new_positions = set()
            for position, f_x, f_y in positions:
                for n in neighbours[position]:
                    new_positions.add((n, f_x, f_y))
                if position[0] == 0:
                    new_positions.add(((width - 1, position[1]), f_x - 1, f_y))
                if position[0] == width - 1:
                    new_positions.add(((0, position[1]), f_x + 1, f_y))
                if position[1] == 0:
                    new_positions.add(((position[0], height - 1), f_x, f_y - 1))
                if position[1] == height - 1:
                    new_positions.add(((position[0], 0), f_x, f_y + 1))
            positions = new_positions
        return positions

    def summarise_fields(field_positions):
        counts = collections.defaultdict(int)
        for _, f_x, f_y in field_positions:
            counts[(f_x, f_y)] += 1
        return counts

    for i, row in enumerate(data):
        if "S" in row:
            start = (i, row.index("S"))
            data[i] = data[i].replace("S", ".")
            break

    # precalc of all neighbours
    neighbours = find_neighbours(data)

    width = len(data[0])
    height = len(data)

    fields = calculate_fields(
        neighbours, width, height, start, steps % width + width * 2
    )  # number of steps chosen by testing "worked for my data"
    counts = summarise_fields(fields)
    tips = counts[(-2, 0)] + counts[(2, 0)] + counts[(0, -2)] + counts[(0, 2)]
    edges_outer = counts[(-2, -1)] + counts[(-2, 1)] + counts[(2, -1)] + counts[(2, 1)]
    edges_inner = counts[(-1, -1)] + counts[(-1, 1)] + counts[(1, -1)] + counts[(1, 1)]
    center_odd = counts[(0, 1)]
    center_even = counts[(0, 0)]
    num = steps // width
    score = (
        tips
        + edges_outer * num
        + edges_inner * (num - 1)
        + center_odd * num**2
        + center_even * (num - 1) ** 2
    )

    return score


if testing:
    if part1:
        test_data_p = parse(test_data)
        res1 = calc(test_data_p, 6)
        ans1 = test_ans1
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")

    # not working with test data for part 2 since it expects the straight open row/column
    # i.e. constant expansion

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
