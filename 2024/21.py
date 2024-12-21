import functools

import requests

day = 21
part1 = True
part2 = True
testing = True
active = True

test_data = """
029A
980A
179A
456A
379A
"""

test_data2 = test_data

test_ans1 = 126384
test_ans2 = 154


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data

def calc(data):
    cpad = {c: (i % 3, i // 3) for i, c in enumerate("789456123x0A")}
    dpad = {c: (i % 3, i // 3) for i, c in enumerate("x^A<v>")}

    def best_dpad(pos, new_pos, drobots):
        tot = float("inf")
        stack = [(pos, "")]

        while stack:
            p, path = stack.pop(0)

            if p == new_pos:
                res = move_robot(path + "A", drobots - 1)
                tot = min(tot, res)
            elif p != dpad["x"]:
                if p[0] < new_pos[0]:
                    stack.append(((p[0] + 1, p[1]), path + ">"))
                elif p[0] > new_pos[0]:
                    stack.append(((p[0] - 1, p[1]), path + "<"))
                if p[1] < new_pos[1]:
                    stack.append(((p[0], p[1] + 1), path + "v"))
                elif p[1] > new_pos[1]:
                    stack.append(((p[0], p[1] - 1), path + "^"))
        return tot

    def move_robot(path, drobots):
        if not drobots:
            return len(path)

        tot = 0
        pos = dpad["A"]

        for c in path:
            new_pos = dpad[c]
            tot += best_dpad(pos, new_pos, drobots)
            pos = new_pos
        return tot

    def cmove(pos, new_pos, drobots):
        tot = float("inf")
        stack = [(pos, "")]

        while stack:
            p, path = stack.pop(0)
            if p == new_pos:
                res = move_robot(path + "A", drobots)
                tot = min(tot, res)
            elif p != cpad["x"]:
                if p[0] < new_pos[0]:
                    stack.append(((p[0] + 1, p[1]), path + ">"))
                elif p[0] > new_pos[0]:
                    stack.append(((p[0] - 1, p[1]), path + "<"))
                if p[1] < new_pos[1]:
                    stack.append(((p[0], p[1] + 1), path + "v"))
                elif p[1] > new_pos[1]:
                    stack.append(((p[0], p[1] - 1), path + "^"))
        return tot

    ans = 0
    for row in data:
        result = 0
        pos = cpad["A"]
        for c in row:
            new_pos = cpad[c]
            result += cmove(pos, new_pos, 2)
            pos = new_pos
        ans += result * int(row[:-1])

    return ans


def calc2(data):
    cpad = {c: (i % 3, i // 3) for i, c in enumerate("789456123x0A")}
    dpad = {c: (i % 3, i // 3) for i, c in enumerate("x^A<v>")}

    @functools.cache
    def best_dpad(pos, new_pos, drobots):
        tot = float("inf")
        stack = [(pos, "")]

        while stack:
            p, path = stack.pop(0)

            if p == new_pos:
                res = move_robot(path + "A", drobots - 1)
                tot = min(tot, res)
            elif p != dpad["x"]:
                if p[0] < new_pos[0]:
                    stack.append(((p[0] + 1, p[1]), path + ">"))
                elif p[0] > new_pos[0]:
                    stack.append(((p[0] - 1, p[1]), path + "<"))
                if p[1] < new_pos[1]:
                    stack.append(((p[0], p[1] + 1), path + "v"))
                elif p[1] > new_pos[1]:
                    stack.append(((p[0], p[1] - 1), path + "^"))
        return tot

    def move_robot(path, drobots):
        if not drobots:
            return len(path)

        tot = 0
        pos = dpad["A"]

        for c in path:
            new_pos = dpad[c]
            tot += best_dpad(pos, new_pos, drobots)
            pos = new_pos
        return tot

    def cmove(pos, new_pos, drobots):
        tot = float("inf")
        stack = [(pos, "")]

        while stack:
            p, path = stack.pop(0)
            if p == new_pos:
                res = move_robot(path + "A", drobots)
                tot = min(tot, res)
            elif p != cpad["x"]:
                if p[0] < new_pos[0]:
                    stack.append(((p[0] + 1, p[1]), path + ">"))
                elif p[0] > new_pos[0]:
                    stack.append(((p[0] - 1, p[1]), path + "<"))
                if p[1] < new_pos[1]:
                    stack.append(((p[0], p[1] + 1), path + "v"))
                elif p[1] > new_pos[1]:
                    stack.append(((p[0], p[1] - 1), path + "^"))
        return tot

    ans = 0
    for row in data:
        result = 0
        pos = cpad["A"]
        for c in row:
            new_pos = cpad[c]
            result += cmove(pos, new_pos, 25)
            pos = new_pos
        ans += result * int(row[:-1])

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
