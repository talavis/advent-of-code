import requests

day = 13
part1 = True
part2 = True
testing = True
active = True

test_data = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

test_data2 = test_data

test_ans1 = 405
test_ans2 = 400


def parse(indata):
    data_rows = indata.split("\n")
    data = []
    part = []
    for row in data_rows:
        if not row:
            if part:
                data.append(part)
            part = []
        else:
            part.append(row)
    return data


def calc(data):
    def find_h_ref(part):
        for i in range(len(part) - 1):
            if part[i] == part[i + 1]:
                b = i - 1
                f = i + 2
                match = True
                while b >= 0 and f < len(part):
                    if part[b] != part[f]:
                        match = False
                        break
                    b -= 1
                    f += 1
                if match:
                    return i + 1
        return 0

    def find_v_ref(part):
        columns = []
        for i in range(len(part[0])):
            columns.append("".join(r[i] for r in part))

        return find_h_ref(columns)

    score = 0
    for part in data:
        if res := find_h_ref(part):
            score += 100 * (res)
        elif res := find_v_ref(part):
            score += res

    return score


def calc2(data):
    def find_v_ref(part):
        columns = []
        for i in range(len(part[0])):
            columns.append("".join(r[i] for r in part))

        return find_h_ref(columns)

    def find_h_ref(part):
        for i in range(len(part) - 1):
            smudge_off = False
            if part[i] == part[i + 1] or ok_diff(part[i], part[i + 1]):
                if ok_diff(part[i], part[i + 1]):
                    smudge_off = True
                b = i - 1
                f = i + 2
                ok = True
                while b >= 0 and f < len(part):
                    if part[b] != part[f]:
                        if not smudge_off and ok_diff(part[b], part[f]):
                            smudge_off = True
                        else:
                            ok = False
                            break
                    b -= 1
                    f += 1
                if ok and smudge_off:
                    return i + 1
        return 0

    def ok_diff(row1, row2):
        d = 0
        for i, j in zip(row1, row2):
            if i != j:
                d += 1
        return d == 1

    score = 0
    for part in data:
        if res := find_h_ref(part):
            score += 100 * (res)
        elif res := find_v_ref(part):
            score += res

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
