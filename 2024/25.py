import requests

day = 25
part1 = True
part2 = False
testing = True
active = True

test_data = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""

test_data2 = test_data

test_ans1 = 3
test_ans2 = 154


def parse(indata):
    data = [part for part in indata.split("\n\n") if part]
    return data


def calc(data):
    locks = []
    keys = []

    for part in data:
        rows = [row for row in part.split("\n") if row]
        height = len(rows)-2
        if "." not in rows[0]:
            entry = "l"
        else:
            entry = "k"
        if entry == "l":
            d = [0]*len(rows[0])
            for i, row in enumerate(rows):
                if i == 0:
                    continue
                for j in range(len(row)):
                    if row[j] == "#":
                        d[j] += 1
            locks.append(d)
        else:
            d = [0]*len(rows[0])
            for i, row in enumerate(rows[::-1]):
                if i == 0:
                    continue
                for j in range(len(row)):
                    if row[j] == "#":
                        d[j] += 1
            keys.append(d)
    ans = 0
    for l in locks:
        for k in keys:
            ok = True
            for i in range(len(l)):
                if k[i] + l[i] > height:
                    ok = False
                    break
            if ok:
                ans += 1
    return ans


def calc2(data):
    ans = 0
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
