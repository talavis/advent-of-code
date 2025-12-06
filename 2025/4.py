import time

import requests

day = 4
part1 = True
part2 = True
testing = True
active = True
timings = True

test_data = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""

test_data2 = test_data

test_ans1 = 13
test_ans2 = 43


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    papers = set()
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == "@":
                papers.add((i, j))

    neighbours = {}
    for paper in papers:
        neighbours[paper] = []
        for d in ((-1, -1), (0, -1), (1, -1), (1, 0),
                  (1, 1), (0, 1), (-1, 1), (-1, 0)):
            pos = (paper[0]+d[0], paper[1]+d[1])
            if pos in papers:
                neighbours[paper].append((pos[0], pos[1]))
    return papers, neighbours


def calc(data):
    ans = 0
    papers, neighbours = data
    for pos in papers:
        nearby = 0
        if len(neighbours[pos]) < 4:
            ans += 1
    return ans


def calc2(data):
    ans = 0
    papers, neighbours = data
    removed = True
    while removed:
        removed = False
        current = set(papers)
        for pos in current:
            nearby = 0
            for n in neighbours[pos]:
                if n in current:
                    nearby += 1
            if nearby < 4:
                papers.remove(pos)
                removed = True
                ans += 1
    return ans

start_total = time.perf_counter()
if testing:
    if part1:
        test_data_p = parse(test_data)
        start_test_part1 = time.perf_counter()
        res1 = calc(test_data_p)
        end_test_part1 = time.perf_counter()
        print(f"Test part 1: {res1} ({test_ans1}){'   !!!' if res1 != test_ans1 else ''}")

    if part2:
        test_data_p2 = parse(test_data2)
        start_test_part2 = time.perf_counter()
        res2 = calc2(test_data_p2)
        end_test_part2 = time.perf_counter()
        print(f"Test part 2: {res2} ({test_ans2}){'   !!!' if res2 != test_ans2 else ''}")

if active:
    with open("cookie.dat") as f:
        cookies = {"session": f.read()}
    try:
        with open(f"{day}.txt") as f:
            raw = f.read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2025/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        start_part1 = time.perf_counter()
        ans = calc(data)
        end_part1 = time.perf_counter()
        print(f"Part 1: {ans}")

    if part2:
        data = parse(raw)
        start_part2 = time.perf_counter()
        ans = calc2(data)
        end_part2 = time.perf_counter()
        print(f"Part 2: {ans}")

end_total = time.perf_counter()

if timings:
    print("Runtime:")
    if part1:
        if testing:
            print(f"Test 1: {end_test_part1 - start_test_part1} seconds")
        if active:
            print(f"Part 1: {end_part1 - start_part1} seconds")
    if part2:
        if testing:
            print(f"Test 2: {end_test_part2 - start_test_part2} seconds")
        if active:
            print(f"Part 2: {end_part2 - start_part2} seconds")
    print(f"Total: {end_total - start_total} seconds")
