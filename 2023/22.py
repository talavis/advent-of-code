import requests

day = 22
part1 = True
part2 = True
testing = True
active = True

test_data = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

test_data2 = test_data

test_ans1 = 5
test_ans2 = 7


def parse(indata):
    data_rows = indata.split("\n")
    data = []
    for row in data_rows:
        if not row:
            continue
        coord = []
        for c in row.split("~"):
            coord.append(tuple(int(val) for val in c.split(",")))
        data.append(tuple(coord))
    return data


def calc(data):
    # assumptions:
    # * no brick is diagonal

    # generate bricks
    bricks = {}
    for e in data:
        bricks[e] = set()
        x = e[0][0]
        y = e[0][1]
        z = e[0][2]
        if e[0][0] - e[1][0] != 0:  # x
            x_low = min(e[0][0], e[1][0])
            x_high = max(e[0][0], e[1][0])
            for x in range(x_low, x_high + 1):
                bricks[e].add((x, y, z))
        elif e[0][1] - e[1][1] != 0:  # y
            y_low = min(e[0][1], e[1][1])
            y_high = max(e[0][1], e[1][1])
            for y in range(y_low, y_high + 1):
                bricks[e].add((x, y, z))
        elif e[0][2] - e[1][2] != 0:  # z
            z_low = min(e[0][2], e[1][2])
            z_high = max(e[0][2], e[1][2])
            for z in range(z_low, z_high + 1):
                bricks[e].add((x, y, z))
        else:  # single cube
            bricks[e].add((x, y, z))

    # fall down
    # must be sorted
    items = bricks.items()
    vals = []
    for item in items:
        vals.append([item[0], min(i[2] for i in item[1])])
    moving = [e[0] for e in sorted(vals, key=lambda x: x[1])]

    stopped = set()
    for k in list(moving):
        z_coords = [c[2] for c in bricks[k]]
        if 1 in z_coords:
            stopped.add(k)
            moving.remove(k)

    while moving:
        coords = set()
        for k in stopped:
            coords.update(bricks[k])
        for k in list(moving):
            coord = bricks[k]
            new_coord = set((c[0], c[1], c[2] - 1) for c in coord)
            z_coord = [c[2] for c in new_coord]
            if new_coord.intersection(coords) or 0 in z_coord:
                coords.update(coord)
                stopped.add(k)
                moving.remove(k)
            else:
                bricks[k] = new_coord

    # find supporters
    coords = {}
    supporters = {}
    for k in bricks:
        for c in bricks[k]:
            coords[c] = k

    for k in bricks:
        supporters[k] = set()

        z_coords = [c[2] for c in bricks[k]]
        if 1 in z_coords:
            supporters[k].add("ground")

        co = bricks[k]
        b = min(c[2] for c in co)
        for c in co:
            if c[2] == b:
                ps = (c[0], c[1], c[2] - 1)
                if ps in coords:
                    supporters[k].add(coords[ps])

    supporting = {}
    for k in supporters:
        supporting[k] = set()

    for k in bricks:
        for s in supporters[k]:
            if s != "ground":
                supporting[s].add(k)

    score = 0
    for k in bricks:
        supported = supporting[k]
        if not supported:
            score += 1
        else:
            crash = False
            for s in supported:
                if len(supporters[s]) == 1:
                    crash = True
                    break
            if not crash:
                score += 1
    return score


def calc2(data):
    bricks = {}
    for e in data:
        bricks[e] = set()
        x = e[0][0]
        y = e[0][1]
        z = e[0][2]
        if e[0][0] - e[1][0] != 0:  # x
            x_low = min(e[0][0], e[1][0])
            x_high = max(e[0][0], e[1][0])
            for x in range(x_low, x_high + 1):
                bricks[e].add((x, y, z))
        elif e[0][1] - e[1][1] != 0:  # y
            y_low = min(e[0][1], e[1][1])
            y_high = max(e[0][1], e[1][1])
            for y in range(y_low, y_high + 1):
                bricks[e].add((x, y, z))
        elif e[0][2] - e[1][2] != 0:  # z
            z_low = min(e[0][2], e[1][2])
            z_high = max(e[0][2], e[1][2])
            for z in range(z_low, z_high + 1):
                bricks[e].add((x, y, z))
        else:  # single cube
            bricks[e].add((x, y, z))

    # fall down
    # sort the bricks
    items = bricks.items()
    vals = []
    for item in items:
        vals.append([item[0], min(i[2] for i in item[1])])
    moving = [e[0] for e in sorted(vals, key=lambda x: x[1])]

    stopped = set()
    for k in list(moving):
        z_coords = [c[2] for c in bricks[k]]
        if 1 in z_coords:
            stopped.add(k)
            moving.remove(k)

    while moving:
        coords = set()
        for k in stopped:
            coords.update(bricks[k])
        for k in list(moving):
            coord = bricks[k]
            new_coord = set((c[0], c[1], c[2] - 1) for c in coord)
            z_coord = [c[2] for c in new_coord]
            if new_coord.intersection(coords) or 0 in z_coord:
                coords.update(coord)
                stopped.add(k)
                moving.remove(k)
            else:
                bricks[k] = new_coord

    # find supporters
    coords = {}
    supporters = {}
    for k in bricks:
        for c in bricks[k]:
            if c in coords:
                print(c)
                print("panic")
            coords[c] = k

    for k in bricks:
        supporters[k] = set()

        z_coords = [c[2] for c in bricks[k]]
        if 1 in z_coords:
            supporters[k].add("ground")

        co = bricks[k]
        b = min(c[2] for c in co)
        for c in co:
            if c[2] == b:
                ps = (c[0], c[1], c[2] - 1)
                if ps in coords:
                    supporters[k].add(coords[ps])

    supporting = {}
    for k in supporters:
        supporting[k] = set()

    for k in bricks:
        for s in supporters[k]:
            if s != "ground":
                supporting[s].add(k)

    to_destroy = set()
    for k in bricks:
        supported = supporting[k]
        for s in supported:
            if len(supporters[s]) == 1:
                to_destroy.add(k)
                break

    def cascade(d, supporters):
        dead = {d}
        lost = True
        while lost:
            lost = False
            for s in list(supporters):
                if s in dead:
                    continue
                a = supporters[s]
                if len(a.intersection(dead)) == len(a):
                    dead.add(s)
                    lost = True

        return len(dead)-1

    score = 0
    for d in to_destroy:
        score += cascade(d, supporters)

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
