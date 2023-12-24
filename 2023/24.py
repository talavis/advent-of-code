import itertools

# import requests
import z3

day = 24
part1 = True
part2 = True
testing = True
active = True

test_data = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

test_data2 = test_data

test_ans1 = 2
test_ans2 = 47


def parse(indata):
    data_rows = indata.split("\n")
    data = []
    for row in data_rows:
        if not row:
            continue
        p1, p2 = row.split("@")
        data.append(
            [[int(p) for p in p1.strip().split(",")], [int(p) for p in p2.strip().split(",")]]
        )
    return data


def calc(data, a_min=200000000000000, a_max=400000000000000):
    def intersect(l1, l2, area_min, area_max):
        # y = kx + m
        # l1: ax + b
        # l2: cx + d
        a = l1[1][1] / l1[1][0]
        b = l1[0][1] - a * l1[0][0]
        c = l2[1][1] / l2[1][0]
        d = l2[0][1] - c * l2[0][0]
        if a == c:
            return False  # paralell
        # ax + b = cx + d
        # ax - cx = d - b
        # x(a - c) = d - b
        # x = (d - b) / (a - c)
        intersection_x = (d - b) / (a - c)
        intersection_y = a * intersection_x + b
        # ignore if in the past
        t1 = (intersection_x - l1[0][0]) / l1[1][0]
        t2 = (intersection_x - l2[0][0]) / l2[1][0]
        if t1 < 0 or t2 < 0:
            return False
        if area_min <= intersection_x <= area_max and area_min <= intersection_y <= area_max:
            return True
        return False

    score = 0
    for l1, l2 in itertools.combinations(data, 2):
        if intersect(l1, l2, a_min, a_max):
            score += 1
    return score


def calc2(data):
    # for each hailstone (h):
    # x + t * xv = h_x + t * h_vx
    # y + t * yv = h_y + t * h_vy
    # z + t * zv = h_z + t * h_vz
    ref_x, ref_y, ref_z = z3.Int("x"), z3.Int("y"), z3.Int("z")
    ref_vx, ref_vy, ref_vz = z3.Int("vx"), z3.Int("vy"), z3.Int("vz")
    solver = z3.Solver()
    for i in range(3):  # 3 might be enough
        t = z3.Int(f"T{i}")
        h_x, h_y, h_z = data[i][0]
        h_vx, h_vy, h_vz = data[i][1]
        solver.add(ref_x + t * ref_vx - h_x - t * h_vx == 0)
        solver.add(ref_y + t * ref_vy - h_y - t * h_vy == 0)
        solver.add(ref_z + t * ref_vz - h_z - t * h_vz == 0)
    res = solver.check()
    model = solver.model()
    return int(repr(model.eval(ref_x + ref_y + ref_z)))


if testing:
    if part1:
        test_data_p = parse(test_data)
        res1 = calc(test_data_p, 7, 27)
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
