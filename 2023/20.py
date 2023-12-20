import collections

import requests

day = 20
part1 = True
part2 = True
testing = True
active = True

test_data1a = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

test_data1b = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""

test_data2 = test_data1a

test_ans1a = 32000000
test_ans1b = 11687500
test_ans2 = -1


def parse(indata):
    data_rows = indata.split("\n")
    tmp = [row for row in data_rows if row]
    data = {}
    for row in tmp:
        p = row.split(" -> ")
        outputs = p[1].split(", ")
        if p[0][0] in ("%", "&"):
            data[p[0][1:]] = [
                p[0][0],
                {},
                outputs,
                False,
            ]  # [type, {inputs}, output, state] inputs - i: state - only &,  state - only %
        else:
            data[p[0]] = ["", [], outputs, False]  # broadcaster
    for key in data:
        for o in data[key][2]:
            if o in data:
                if data[o][0] == "&":
                    data[o][1][key] = False
    return data


def calc(data):
    high = 0
    low = 0
    for i in range(1000):
        q = collections.deque()
        low += 1
        for o in data["broadcaster"][2]:
            low += 1
            q.append([o, False, "broadcaster"])
        a = 0
        while q:
            c, signal, origin = q.popleft()
            if c in data:
                current = data[c]
            else:
                current = ["", [], [], False]
            if current[0] == "%":
                if not signal:
                    current[3] = not current[3]
                    for o in current[2]:
                        if current[3]:
                            high += 1
                        else:
                            low += 1
                        q.append([o, current[3], c])
            elif current[0] == "&":
                data[c][1][origin] = signal
                if all(data[c][1].values()):
                    state = False
                else:
                    state = True
                for o in current[2]:
                    if state:
                        high += 1
                    else:
                        low += 1
                    q.append([o, state, c])
    score = low * high
    return score


def calc2(data):
    def gcd(values):
        divs = []
        for v in values:
            divs.append(find_divisors(v))
        res = []
        for d in divs:
            for v in d:
                while res.count(v) < d.count(v):
                    res.append(v)
        return res

    def find_divisors(value):
        i = 2
        divs = []
        while value >= i:
            if value % i == 0:
                divs.append(i)
                value //= i
            else:
                i += 1
        return divs

    rx_low = 0
    i = 0
    last = {}
    gaps = {}
    while rx_low != 1:
        i += 1
        q = collections.deque()
        for o in data["broadcaster"][2]:
            q.append([o, False, "broadcaster"])
        a = 0
        while q:
            c, signal, origin = q.popleft()
            if c in data:
                current = data[c]
                if c == "rx" and not signal:
                    rx_low += 1
            else:
                current = ["", [], [], False]
            if current[0] == "%":
                if not signal:
                    current[3] = not current[3]
                    for o in current[2]:
                        q.append([o, current[3], c])
            elif current[0] == "&":
                data[c][1][origin] = signal
                if c == "bq":
                    for k, v in data[c][1].items():
                        if v:
                            if k in last and i - last[k] != 0:
                                gaps[k] = i - last[k]
                            last[k] = i
                        # hardcoded for my input; there were four inputs to the one leading to rx
                        if len(gaps) == 4:
                            if all(gaps.values()):
                                score = 1
                                for v in gcd(gaps.values()):
                                    score *= v
                                return score
                if all(data[c][1].values()):
                    state = False
                else:
                    state = True
                for o in current[2]:
                    q.append([o, state, c])


if testing:
    if part1:
        test_data_p1a = parse(test_data1a)
        res1a = calc(test_data_p1a)
        ans1a = test_ans1a
        print(f"Test part 1a: {res1a} ({ans1a}){'   !!!' if res1a != ans1a else ''}")
        test_data_p1b = parse(test_data1b)
        res1b = calc(test_data_p1b)
        ans1b = test_ans1b
        print(f"Test part 1b: {res1b} ({ans1b}){'   !!!' if res1b != ans1b else ''}")

if active:
    cookies = {"session": open("cookie.dat").read()}
    try:
        raw = open(f"{day}.txt").read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2023/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
