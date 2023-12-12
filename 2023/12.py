import functools

import requests

day = 12
part1 = True
part2 = True
testing = True
active = True

test_data = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

test_data2 = test_data

test_ans1 = 21
test_ans2 = 525152


def parse(indata):
    data_rows = indata.split("\n")
    data = [row.split() for row in data_rows if row]
    for i in range(len(data)):
        data[i][1] = [int(e) for e in data[i][1].split(",")]
        data[i][0] = list(data[i][0])
    return data


def calc(data):
    def gen(dat, combo):
        score = 0
        if "?" in dat:
            i = dat.index("?")
            new_dat = list(dat)
            new_dat[i] = "#"
            score += gen(new_dat, combo)
            new_dat[i] = "."
            score += gen(new_dat, combo)
        else:
            dat = "".join(dat)
            broken = [len(b) for b in dat.split(".") if b]
            if broken == combo:
                score = 1
            else:
                score = 0

        return score

    score = 0
    for row in data:
        score += gen(row[0], row[1])

    return score


def calc2(data):
    @functools.lru_cache
    def gen(dat, combo):
        if not dat:
            if combo:
                return 0
            else:
                return 1
        if dat[0] == ".":  # jump to next potential spring
            return gen(dat.strip("."), combo)
        if dat[0] == "?":  # test alternatives
            return gen(dat.replace("?", ".", 1), combo) + gen(dat.replace("?", "#", 1), combo)
        if dat[0] == "#":
            if not combo:  # no expected springs remaining
                return 0
            if len(dat) < combo[0]:  # too short for next spring
                return 0
            if "." in dat[0 : combo[0]]:  # current segment too short for next spring
                return 0
            if len(combo) > 1:
                if len(dat) < combo[0] + 1 or dat[combo[0]] == "#":  # more springs, not long enough
                    return 0
                # since the current segment is # or ?, all ? must be # to match req, must be space at end
                return gen(dat[combo[0] + 1 :], combo[1:])
            else:
                # last group, "one" more iteration to verify that there is no issue with the remains
                return gen(dat[combo[0] :], combo[1:])

    score = 0
    for row in data:
        new_row = "?".join(["".join(row[0])] * 5)
        score += gen(new_row, tuple(row[1] * 5))
    return score


if testing:
    test_data_p = parse(test_data)

    if part1:
        res1 = calc(test_data_p)
        ans1 = test_ans1
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")

    test_data_p2 = parse(test_data2)
    if part2:
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
    data = parse(raw)
    if part1:
        print(f"Part 1: {calc(data)}")
    data = parse(raw)
    if part2:
        print(f"Part 2: {calc2(data)}")
