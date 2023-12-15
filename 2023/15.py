import requests

day = 15
part1 = True
part2 = True
testing = True
active = True

test_data = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

test_data2 = test_data

test_ans1 = 1320
test_ans2 = 145


def parse(indata):
    data_rows = indata.split("\n")
    data = [row.split(",") for row in data_rows if row][0]
    return data


def calc(data):
    def hash_func(text):
        score = 0
        for c in text:
            score += ord(c)
            score *= 17
            score = score % 256
        return score

    score = 0
    for p in data:
        score += hash_func(p)
    return score


def calc2(data):
    def hash_func(text):
        score = 0
        for c in text:
            score += ord(c)
            score *= 17
            score = score % 256
        return score

    boxes = [[[], []] for _ in range(256)]
    for p in data:
        if "=" in p:
            l, f = p.split("=")
            f = int(f)
            box = hash_func(l)
            if l in boxes[box][0]:
                a = boxes[box][0].index(l)
                boxes[box][1][a] = f
            else:
                boxes[box][0].append(l)
                boxes[box][1].append(f)
        elif "-" in p:
            label = p[: p.index("-")]
            box = hash_func(label)
            if label in boxes[box][0]:
                a = boxes[box][0].index(label)
                boxes[box][0].pop(a)
                boxes[box][1].pop(a)

    score = 0
    for i, b in enumerate(boxes):
        for j, s in enumerate(b[0]):
            score += (i + 1) * (j + 1) * b[1][j]

    return score


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
        raw = requests.get(f"https://adventofcode.com/2023/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
