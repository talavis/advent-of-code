import time

import requests

day = 6
part1 = True
part2 = True
testing = True
active = True
timings = True

test_data = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +
"""

test_data2 = test_data

test_ans1 = 4277556
test_ans2 = 3263827


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data


def calc(data):
    data = [row.split() for row in data if row]
    ans = 0
    for i in range(len(data[0])):
        col = [int(row[i]) for row in data[:-1]]
        if data[-1][i] == "+":
            tot = sum(col)
            ans += tot
            
        else:
            tot = 1
            for val in col:
                tot *= val
            ans += tot
    return ans


def calc2(data):
    row_gaps = []
    for row in data:
        gaps = set()
        for i in range(len(row)):
            if row[i] == " ":
                gaps.add(i)
        row_gaps.append(gaps)
    intersect = row_gaps[0]
    for gaps in row_gaps:
        intersect = intersect & gaps
    gaps = sorted(intersect)
    gaps = [-1] + gaps + [len(data[0])]

    operators = data[-1].split()
    ans = 0
    
    for i in range(1, len(gaps)):
        b = gaps[i-1]
        e = gaps[i]
        vals = []
        for j in range(b+1, e):
            vals.append("")
            for row in data[:-1]:
                vals[-1] += row[j]
        vals = [int(val) for val in vals]

        if operators[i-1] == "+":
            tot = sum(vals)
            ans += tot
        else:
            tot = 1
            for val in vals:
                tot *= val
            ans += tot
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
