import requests

day = 14
part1 = True
part2 = True
testing = True
active = True

test_data = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

test_data2 = test_data

test_ans1 = 12
test_ans2 = 154


def parse(indata):
    data_rows = indata.split("\n")
    data = []
    for row in data_rows:
        if not row:
            continue
        data.append([])
        cols = row.split()
        for c in cols:
            data[-1].append(tuple(int(a) for a in c.split("=")[1].split(",")))
    return data


def calc(data, size=(101, 103)):
    rs = [r[0] for r in data]
    vs = [r[1] for r in data]
    for s in range(100):
        for i in range(len(rs)):
            new_x = rs[i][0] + vs[i][0]
            if new_x < 0:
                new_x = size[0] + new_x
            if new_x >= size[0]:
                new_x = new_x - size[0]

            new_y = rs[i][1] + vs[i][1]
            if new_y < 0:
                new_y = size[1] + new_y
            if new_y >= size[1]:
                new_y = new_y - size[1]
            rs[i] = (new_x, new_y)

    xdiv = size[0] // 2
    ydiv = size[1] // 2
    qs = [0] * 4
    for r in rs:
        q = [-1, -1]
        if r[0] < xdiv:
            q[0] = 0
        elif r[0] > xdiv:
            q[0] = 1
        if r[1] < ydiv:
            q[1] = 0
        elif r[1] > ydiv:
            q[1] = 1
        if -1 in q:
            continue
        qs[q[0] + 2 * q[1]] += 1

    ans = 1
    for q in qs:
        ans *= q
    return ans


def calc2(data, size=(101, 103)):
    # assume the state with the row with the highest number of unique robot positions forms the tree
    # assume it happens within 20000 steps
    rs = [r[0] for r in data]
    vs = [r[1] for r in data]
    highest = 0
    best = 0
    s = 0
    while s < 20000:
        s += 1
        for i in range(len(rs)):
            new_x = rs[i][0] + vs[i][0]
            if new_x < 0:
                new_x = size[0] + new_x
            if new_x >= size[0]:
                new_x = new_x - size[0]

            new_y = rs[i][1] + vs[i][1]
            if new_y < 0:
                new_y = size[1] + new_y
            if new_y >= size[1]:
                new_y = new_y - size[1]
            rs[i] = (new_x, new_y)

        per_row = {}
        for r in rs:
            if r[1] in per_row:
                per_row[r[1]].add(r[0])
            else:
                per_row[r[1]] = {r[0]}
        rowls = []
        for r in per_row:
            rowls.append(len(per_row[r]))

        if max(rowls) > highest:
            highest = max(rowls)
            best = s
            for i in range(size[1]):
                row = ["."] * size[0]
                if i in per_row:
                    for r in per_row[i]:
                        row[r] = "+"
                print("".join(row))
            print()
    return best


if testing:
    if part1:
        test_data_p = parse(test_data)
        res1 = calc(test_data_p, size=(11, 7))
        ans1 = test_ans1
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")

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
