import collections

import requests

day = 23
part1 = True
part2 = True
testing = True
active = True

test_data = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""

test_data2 = test_data

test_ans1 = 94
test_ans2 = 154


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data):
    def find_neighbours(data):
        neighbours = {}
        dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))  # urdl
        slopes = ("^", ">", "v", "<")
        r_len = len(data)
        c_len = len(data[0])

        for i in range(len(data)):
            for j in range(len(data)):
                pos = (i, j)
                neighbours[pos] = set()
                p_type = data[i][j]
                if p_type == ".":
                    for d in dirs:
                        n_pos = (pos[0] + d[0], pos[1] + d[1])
                        if 0 <= n_pos[0] < r_len and 0 <= n_pos[1] < c_len:
                            if data[n_pos[0]][n_pos[1]] != "#":
                                neighbours[pos].add(n_pos)

                elif p_type in slopes:
                    d = slopes.index(p_type)
                    n_pos = (pos[0] + dirs[d][0], pos[1] + dirs[d][1])
                    neighbours[pos].add(n_pos)
        return neighbours

    r_len = len(data)
    c_len = len(data[0])
    start = (0, data[0].index("."))
    end = (r_len - 1, data[r_len - 1].index("."))
    dists = collections.defaultdict(int)
    neighbours = find_neighbours(data)
    q = [(start, 0, set())]
    while q:
        pos, dist, visited = q.pop()
        visited.add(pos)
        if dists[pos] < dist:
            dists[pos] = dist
        dist += 1
        for n in neighbours[pos]:
            if n not in visited:
                q.append((n, dist, set(visited)))
    return dists[end]


def calc2(data):
    def find_neighbours(data):
        neighbours = {}
        dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))  # urdl
        r_len = len(data)
        c_len = len(data[0])

        for i in range(len(data)):
            for j in range(len(data)):
                pos = (i, j)
                p_type = data[i][j]
                if p_type != "#":
                    neighbours[pos] = [[], []]  # node, dist
                    for d in dirs:
                        n_pos = (pos[0] + d[0], pos[1] + d[1])
                        if 0 <= n_pos[0] < r_len and 0 <= n_pos[1] < c_len:
                            if data[n_pos[0]][n_pos[1]] != "#":
                                neighbours[pos][0].append(n_pos)
                                neighbours[pos][1].append(1)
        return neighbours

    def truncate(neighbours, start):
        for k in neighbours.keys():
            kn = neighbours[k]
            if len(kn[0]) == 2:
                n1 = kn[0][0]
                n1d = kn[1][0]
                n2 = kn[0][1]
                n2d = kn[1][1]
                n1n = neighbours[n1]
                n2n = neighbours[n2]
                n1i = n1n[0].index(k)
                n2i = n2n[0].index(k)
                n1n[0].append(n2)
                n1n[1].append(n2d + n1d)
                n2n[0].append(n1)
                n2n[1].append(n1d + n2d)
                n1n[0].pop(n1i)
                n1n[1].pop(n1i)
                n2n[0].pop(n2i)
                n2n[1].pop(n2i)

    neighbours = find_neighbours(data)
    start = (0, data[0].index("."))
    end = (len(data) - 1, data[-1].index("."))
    truncate(neighbours, start)  # in-place path truncation

    dists = collections.defaultdict(int)

    q = [(start, 0, set())]
    while q:
        pos, dist, visited = q.pop()
        visited.add(pos)
        if dists[pos] < dist:
            dists[pos] = dist
        neigh = neighbours[pos]
        for i in range(len(neigh[0])):
            if neigh[0][i] not in visited:
                q.append((neigh[0][i], dist + neigh[1][i], set(visited)))
    return dists[end]


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
