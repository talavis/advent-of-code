import requests

day = 22
part1 = True
part2 = True
testing = True
active = True

test_data = """
1
10
100
2024
"""

test_data2 = """
1
2
3
2024
"""

test_ans1 = 37327623
test_ans2 = 23


def parse(indata):
    data_rows = indata.split("\n")
    data = [int(row) for row in data_rows if row]
    return data


def calc(data):
    def mp(x, y):
        return (x ^ y) % 16777216

    ans = 0
    for d in data:
        a = d
        for i in range(2000):
            x = a * 64
            a = mp(a, x)
            y = a // 32
            a = mp(a, y)
            z = a * 2048
            a = mp(a, z)
        ans += a
    return ans


def calc2(data):
    def mp(x, y):
        return (x ^ y) % 16777216

    ans = 0
    seqs = {}
    for irow, d in enumerate(data):
        a = d
        prices = [a % 10]
        for i in range(2000):
            x = a * 64
            a = mp(a, x)
            y = a // 32
            a = mp(a, y)
            z = a * 2048
            a = mp(a, z)
            prices.append(a % 10)

        changes = [None, None, None, None]
        for i, p in enumerate(prices):
            changes.pop(0)
            if changes[-1] is None:
                changes.append(p)
            else:
                changes.append(p - prices[i - 1])
            if None not in changes:
                c = tuple(changes)
                if c not in seqs:
                    seqs[c] = [-1] * len(data)
                    seqs[c][irow] = p
                elif seqs[c][irow] == -1:
                    seqs[c][irow] = p

    best = 0
    for s in seqs:
        a = sum(v for v in seqs[s] if v != -1)
        if a > best:
            best = a
    return best


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
