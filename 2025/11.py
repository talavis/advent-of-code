import time

import requests
import functools

day = 11
part1 = True
part2 = True
testing = True
active = True
timings = False

test_data = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

test_data2 = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""

test_ans1 = 5
test_ans2 = 2


def parse(indata):
    data_rows = indata.split("\n")
    data = {}
    for row in data_rows:
        if not row:
            continue
        cols = row.split()
        data[cols[0][:-1]] = cols[1:]
    return data


def calc(data):
    def step(identifier):
        ans = 0
        if data[identifier] == ["out"]:
            return 1
        for new_id in data[identifier]:
            ans += step(new_id)
        return ans

    return step("you")


def calc2(data):
    @functools.cache
    def step(identifier, dac, fft):
        if data[identifier] == ["out"]:
            if dac and fft:
                return 1
            else:
                return 0
        if identifier == "dac":
            dac = True
        if identifier == "fft":
            fft = True
        ans = 0
        for new_id in data[identifier]:
            ans += step(new_id, dac, fft)
        return ans

    return step("svr", False, False)


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
