import functools

import requests

day = 11
part1 = True
part2 = True
testing = True
active = True

test_data = """
125 17
"""

test_data2 = test_data

test_ans1 = 55312
test_ans2 = -1


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row][0].split()
    return data


def calc(data):
    stones = data[:]
    for i in range(25):
        new_stones = []
        for stone in stones:
            sl = len(stone)
            if sl % 2 == 0:
                new_stones.append(stone[: sl // 2])
                new_stones.append(str(int(stone[sl // 2 :])))
            elif stone == "0":
                new_stones.append("1")
            else:
                new_stones.append(str(int(stone) * 2024))
        stones = new_stones
    return len(stones)


def calc2(data):
    @functools.cache
    def blink(stone, steps):
        if steps == 0:
            return 1
        if stone == "0":
            return blink("1", steps - 1)
        sl = len(stone)
        if sl % 2 == 0:
            return blink(stone[: sl // 2], steps - 1) + blink(str(int(stone[sl // 2 :])), steps - 1)
        return blink(str(int(stone) * 2024), steps - 1)

    ans = 0
    for stone in data:
        ans += blink(stone, 75)
    return ans


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
        raw = requests.get(f"https://adventofcode.com/2024/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
