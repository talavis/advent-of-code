import time

import requests

day = 5
part1 = True
part2 = True
testing = True
active = True
timings = True

test_data = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

test_data2 = test_data

test_ans1 = 3
test_ans2 = 14


def parse(indata):
    ranges = []
    ingredients = []

    row_parts = indata.split("\n\n")
    for row in row_parts[0].split("\n"):
        if not row:
            continue
        a = row.split("-")
        ranges.append((int(a[0]), int(a[1])))
    for row in row_parts[1].split("\n"):
        if not row:
            continue
        ingredients.append(int(row))
        
    return ranges, ingredients


D = open("5.txt").read()
ranges, ingredients = D.split('\n\n')
R = []
for r in ranges.splitlines():
    st,ed = r.split('-')
    st = int(st)
    ed = int(ed)
    R.append((st,ed))


def calc(data):
    ranges, ingredients = data
    fresh = []
    for i in ingredients:
        for b, e in ranges:
            if b <= i <= e:
                fresh.append(i)
                break
    return len(fresh)


def calc2(data):
    ranges, _ = data

    ranges.sort()
    pos = 0
    ans = 0

    for b, e in ranges:
        if pos >= b:
            b = pos+1
        if b <= e:
            ans += e-b+1
        pos = max(pos, e)
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
