import time

import requests
from shapely.geometry import Polygon
from shapely.prepared import prep

day = 9
part1 = True
part2 = True
testing = True
active = True
timings = True

test_data = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

test_data2 = test_data

test_ans1 = 50
test_ans2 = 24


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    for i in range(len(data)):
        data[i] = [int(val) for val in data[i].split(",")]
    return data


def calc(data):
    ans = 0
    for c1 in data:
        for c2 in data:
            s1 = abs(c1[0]-c2[0])+1
            s2 = abs(c1[1]-c2[1])+1
            area = s1*s2
            if area > ans:
                ans = area
    return ans


def calc2(data):
    polygon = Polygon(data)
    prep_polygon = prep(polygon)
    ans = 0
    for c1 in data:
        for c2 in data:
            rectangle = Polygon((c1, (c1[0], c2[1]), c2, (c2[0], c1[1])))
            s1 = abs(c1[0]-c2[0])+1
            s2 = abs(c1[1]-c2[1])+1
            area = s1*s2
            if area > ans and prep_polygon.covers(rectangle):
                ans = area
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
