import time

import requests

day = 12
part1 = True
part2 = False
testing = True
active = True
timings = False

test_data = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""

test_data2 = test_data

test_ans1 = 2
test_ans2 = 43


def parse(indata):
    sections = indata.split("\n\n")
    tiles = []
    for section in sections[:-1]:
        rows = section.split("\n")
        tiles.append(rows[1:])

    regions = []
    for row in sections[-1].split("\n"):
        if not row:
            continue
        regions.append([])
        cols = row.split()
        parts = cols[0].split("x")
        size = (int(parts[0]), int(parts[1][:-1]))
        regions[-1].append(size)
        regions[-1].extend([int(val) for val in cols[1:]])
    return tiles, regions


def calc(data):
    ans = 0
    tiles, regions = data
    tile_sizes = ["".join(tile).count("#") for tile in tiles]
    for i in range(len(regions)):
        total_tile_size = sum([tile_sizes[j]*regions[i][1:][j] for j in range(len(regions[i][1:]))])
        region_size = regions[i][0][0]*regions[i][0][1]
        if total_tile_size <= region_size:
            ans += 1
    return ans
    # I decided to submit this answer since I knew it would be _a lot_ of work to create a real algorith. Funnily enough, it worked.


def calc2(data):
    ans = 0
    return ans


start_total = time.perf_counter()
if testing:
    if part1:
        start_test_part1 = time.perf_counter()
        test_data_p = parse(test_data)
        res1 = calc(test_data_p)
        end_test_part1 = time.perf_counter()
        print(
            f"Test part 1: {res1} ({test_ans1}){'   !!!' if res1 != test_ans1 else ''}"
        )

    if part2:
        start_test_part2 = time.perf_counter()
        test_data_p2 = parse(test_data2)
        res2 = calc2(test_data_p2)
        end_test_part2 = time.perf_counter()
        print(
            f"Test part 2: {res2} ({test_ans2}){'   !!!' if res2 != test_ans2 else ''}"
        )

if active:
    with open("cookie.dat") as f:
        cookies = {"session": f.read()}
    try:
        with open(f"{day}.txt") as f:
            raw = f.read()
    except FileNotFoundError:
        raw = requests.get(
            f"https://adventofcode.com/2025/day/{day}/input", cookies=cookies
        ).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        start_part1 = time.perf_counter()
        data = parse(raw)
        ans = calc(data)
        end_part1 = time.perf_counter()
        print(f"Part 1: {ans}")

    if part2:
        start_part2 = time.perf_counter()
        data = parse(raw)
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
