import math
import time

import requests

day = 8
part1 = True
part2 = True
testing = True
active = True
timings = False

test_data = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

test_data2 = test_data

test_ans1 = 40
test_ans2 = 25272


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    for i in range(len(data)):
        data[i] = tuple(int(val) for val in data[i].split(","))
    return data


def calc(data, n_connect=1000):
    connections = set()
    for d in data:
        for e in data:
            if e == d:
                continue
            dist = math.sqrt(
                (d[0] - e[0]) ** 2 + (d[1] - e[1]) ** 2 + (d[2] - e[2]) ** 2
            )
            connections.add((min(d, e), max(d, e), dist))
    sorted_connections = sorted(connections, key=lambda x: x[2])

    circuits = []
    n = 0
    while n < n_connect:
        pos1 = sorted_connections[n][0]
        pos2 = sorted_connections[n][1]
        n += 1
        circ1 = -1
        circ2 = -1
        for i, circ in enumerate(circuits):
            if pos1 in circ:
                circ1 = i
            if pos2 in circ:
                circ2 = i
        if circ1 >= 0 and circ2 >= 0:
            if circ1 == circ2:
                continue
            circuits[circ1] = circuits[circ1].union(circuits[circ2])
            circuits.pop(circ2)
        elif circ1 >= 0:
            circuits[circ1].add(pos2)
        elif circ2 >= 0:
            circuits[circ2].add(pos1)
        else:
            circuits.append({pos1, pos2})

    circuits.sort(key=lambda x: len(x), reverse=True)

    ans = 1
    for i in range(3):
        ans *= len(circuits[i])
    return ans


def calc2(data):
    connections = set()
    for d in data:
        for e in data:
            if e == d:
                continue
            dist = math.sqrt(
                (d[0] - e[0]) ** 2 + (d[1] - e[1]) ** 2 + (d[2] - e[2]) ** 2
            )
            connections.add((min(d, e), max(d, e), dist))
    sorted_connections = sorted(connections, key=lambda x: x[2])

    circuits = []
    n = 0
    ans = 0
    while not n or len(circuits[0]) < len(data):
        pos1 = sorted_connections[n][0]
        pos2 = sorted_connections[n][1]
        n += 1
        circ1 = -1
        circ2 = -1
        for i, circ in enumerate(circuits):
            if pos1 in circ:
                circ1 = i
            if pos2 in circ:
                circ2 = i
        if circ1 >= 0 and circ2 >= 0:
            if circ1 == circ2:
                continue
            circuits[circ1] = circuits[circ1].union(circuits[circ2])
            circuits.pop(circ2)
        elif circ1 >= 0:
            circuits[circ1].add(pos2)
        elif circ2 >= 0:
            circuits[circ2].add(pos1)
        else:
            circuits.append({pos1, pos2})
        ans = pos1[0] * pos2[0]
    return ans


start_total = time.perf_counter()
if testing:
    if part1:
        start_test_part1 = time.perf_counter()
        test_data_p = parse(test_data)
        res1 = calc(test_data_p, 10)
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
