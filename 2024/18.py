import requests

day = 18
part1 = True
part2 = True
testing = True
active = True

test_data = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

test_data2 = test_data

test_ans1 = 22
test_ans2 = (6, 1)


def parse(indata):
    data_rows = indata.split("\n")
    data = []
    for row in data_rows:
        if not row:
            continue
        cols = row.split(",")
        data.append((int(cols[0]), int(cols[1])))
    return data


def calc(data, side=71, steps=1024):
    blocks = set()
    for i in range(steps):
        blocks.add((data[i][1], data[i][0]))
    scores = []
    for i in range(side):
        for j in range(side):
            scores.append([float("inf"), (i, j)])

    visited = set()
    scores[0][0] = 0
    dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))

    end = (side - 1, side - 1)
    while True:
        ordered = sorted(scores)
        score = ordered[len(visited)][0]
        pos = ordered[len(visited)][1]
        visited.add(pos)
        if pos == end:
            return score
        for d in dirs:
            n = (pos[0] + d[0], pos[1] + d[1])
            if n not in visited and n not in blocks:
                if 0 <= n[0] < side and 0 <= n[1] < side:
                    if scores[n[0] * side + n[1]][0] > score + 1:
                        scores[n[0] * side + n[1]][0] = score + 1
    return ans


# def calc2(data, side=71, start=1024):
def calc2(data, side=71, start=2500):
    blocks = set()
    for i in range(start):
        blocks.add((data[i][1], data[i][0]))
    scores = []
    for i in range(side):
        for j in range(side):
            scores.append([float("inf"), (i, j)])

    visited = set()
    scores[0][0] = 0
    dirs = ((-1, 0), (0, 1), (1, 0), (0, -1))

    end = (side - 1, side - 1)
    step = start

    scores_orig = scores
    while len(data) > len(blocks):
        blocks.add((data[step][1], data[step][0]))
        step += 1
        print(step)
        scores = [list(v) for v in scores_orig]
        visited = set()
        res = 0
        while True:
            ordered = sorted(scores)
            score = ordered[len(visited)][0]
            pos = ordered[len(visited)][1]
            visited.add(pos)
            if pos == end:
                res = score
                break
            for d in dirs:
                n = (pos[0] + d[0], pos[1] + d[1])
                if n not in visited and n not in blocks:
                    if 0 <= n[0] < side and 0 <= n[1] < side:
                        if scores[n[0] * side + n[1]][0] > score + 1:
                            scores[n[0] * side + n[1]][0] = score + 1
        if res == float("inf"):
            return data[step - 1]
    return -1


if testing:
    if part1:
        test_data_p = parse(test_data)
        res1 = calc(test_data_p, side=7, steps=12)
        ans1 = test_ans1
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")

    if part2:
        test_data_p2 = parse(test_data2)
        res2 = calc2(test_data_p2, side=7, start=12)
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
