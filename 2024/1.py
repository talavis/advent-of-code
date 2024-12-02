import requests

day = 1
part1 = True
part2 = True
testing = True
active = True


def parse(indata):
    data_rows = indata.split("\n")
    data = []
    for row in data_rows:
        if not row:
            continue
        cols = row.split()
        data.append([int(cols[0]), int(cols[1])])
    return data


def calc(data):
    c1 = sorted(r[0] for r in data)
    c2 = sorted(r[1] for r in data)
    tot_distance = 0
    for i in range(len(c1)):
        tot_distance += abs(c1[i]-c2[i])
    return tot_distance


def calc2(data):
    c1 = sorted(r[0] for r in data)
    c2 = sorted(r[1] for r in data)
    sim_score = 0
    for c in c1:
        sim_score += c*c2.count(c)
    return sim_score


test_data = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

test_data2 = test_data

if testing:
    test_data = parse(test_data)

    if part1:
        res1 = calc(test_data)
        ans1 = 11
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    if part2:
        test_data2 = parse(test_data2)
        res2 = calc2(test_data2)
        ans2 = 31
        print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

if active:
    cookies = {"session": open("cookie.dat").read()}
    try:
        raw = open(f"{day}.txt").read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2024/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    data = parse(raw)
    if part1:
        print(f"Part 1: {calc(data)}")
    if part2:
        print(f"Part 2: {calc2(data)}")
