import queue

import requests

day = 20
part1 = True
part2 = True
testing = True
active = True

test_data = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

test_data2 = test_data

test_ans1 = 44
test_ans2 = 285


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data, limit=100):
    def distances(start, area):
        dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
        
        dists = [[0]*len(area[0]) for _ in range(len(area))]
        for i in range(len(area)):
            for j in range(len(area[i])):
                if area[i][j] == "#":
                    dists[i][j] = float("inf")

        q = queue.Queue()
        q.put(start)
        visited = {start}

        while not q.empty():
            pos = q.get()
            for d in dirs:
                p = (pos[0]+d[0], pos[1]+d[1])
                if 0 <= p[0] < len(area) and 0 <= p[1] < len(area[0]):
                    if p not in visited and area[p[0]][p[1]] != "#":
                        visited.add(p)
                        dists[p[0]][p[1]] = dists[pos[0]][pos[1]] + 1
                        q.put(p)
        return dists

    def search(pos, base, dists_s, dists_e, dist=2):
        dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
        cheats = set()
        for d in dirs:
            for e in dirs:
                p = (pos[0] + d[0] + e[0], pos[1] + d[1] + e[1])
                if 0 <= p[0] < len(dists_s) and 0 <= p[1] < len(dists_s[0]):
                    if base - (val := dists_s[pos[0]][pos[1]] + dists_e[p[0]][p[1]] + 2) >= limit:
                        cheats.add((pos, p, base-val))
        return cheats
    
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == "S":
                start = (i, j)
            elif c == "E":
                end = (i, j)

    dists_s = distances(start, data)
    dists_e = distances(end, data)

    base = dists_s[end[0]][end[1]]

    cheats = set()
    for i in range(len(dists_s)):
        for j in range(len(dists_s[0])):
            if data[i][j] != "#":
                cheats = cheats.union(search((i, j), base, dists_s, dists_e))

    return len(cheats)
                                      


def calc2(data, limit=100):
    def distances(start, area):
        dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))
        
        dists = [[0]*len(area[0]) for _ in range(len(area))]
        for i in range(len(area)):
            for j in range(len(area[i])):
                if area[i][j] == "#":
                    dists[i][j] = float("inf")

        q = queue.Queue()
        q.put(start)
        visited = {start}

        while not q.empty():
            pos = q.get()
            for d in dirs:
                p = (pos[0]+d[0], pos[1]+d[1])
                if 0 <= p[0] < len(area) and 0 <= p[1] < len(area[0]):
                    if p not in visited and area[p[0]][p[1]] != "#":
                        visited.add(p)
                        dists[p[0]][p[1]] = dists[pos[0]][pos[1]] + 1
                        q.put(p)
        return dists

    def search(pos, base, dists_s, dists_e, dist=2):
        cheats = set()
        for i in range(-20, 21):
            for j in range(-(20-abs(i)), 21-abs(i)):
                p = (pos[0] + i, pos[1] + j)
                if 0 <= p[0] < len(dists_s) and 0 <= p[1] < len(dists_s[0]):
                    if base - (val := dists_s[pos[0]][pos[1]] + dists_e[p[0]][p[1]] + abs(i) + abs(j)) >= limit:
                        cheats.add((pos, p, base-val))
        return cheats
    
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == "S":
                start = (i, j)
            elif c == "E":
                end = (i, j)

    dists_s = distances(start, data)
    dists_e = distances(end, data)

    base = dists_s[end[0]][end[1]]

    cheats = set()
    for i in range(len(dists_s)):
        for j in range(len(dists_s[0])):
            if data[i][j] != "#":
                cheats = cheats.union(search((i, j), base, dists_s, dists_e))
    return len(cheats)


if testing:
    if part1:
        test_data_p = parse(test_data)
        res1 = calc(test_data_p, limit=1)
        ans1 = test_ans1
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")

    if part2:
        test_data_p2 = parse(test_data2)
        res2 = calc2(test_data_p2, limit=50)
        ans2 = test_ans2
        print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

if active:
    with open("cookie.dat") as f:
        cookies = {"session": f.read()}
    try:
        with open(f"{day}.txt") as f:
            raw = f.read()
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
