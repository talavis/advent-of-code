import heapq

import requests

day = 17
part1 = True
part2 = True
testing = True
active = True

test_data = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

test_data2 = test_data

test_ans1 = 102
test_ans2 = 94


def parse(indata):
    data_rows = indata.split("\n")
    data = [[int(value) for value in row] for row in data_rows if row]
    return data


def calc(data):
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # urdl

    to_visit = [(0, 0, 0, -1)]  # start in upper left corner
    visited = set()
    losses = {}

    goal = [len(data) - 1, len(data[0]) - 1]
    while to_visit:
        loss, x, y, ori = heapq.heappop(to_visit)
        if x == goal[0] and y == goal[1]:
            return loss
        if (x, y, ori) in visited:
            continue
        visited.add((x, y, ori))

        for d in range(4):
            loss_inc = 0
            if d == ori or (d + 2) % 4 == ori:
                continue
            for dist in range(1, 4):
                new_x = x + dirs[d][0] * dist
                new_y = y + dirs[d][1] * dist

                if 0 <= new_x < len(data) and 0 <= new_y < len(data[0]):
                    loss_inc += data[new_x][new_y]
                    new_loss = loss + loss_inc

                    group = (new_x, new_y, d)
                    if group in losses:
                        if losses[group] <= new_loss:
                            continue  # old one is better
                        losses[group] = new_loss
                    else:
                        losses[group] = new_loss

                    heapq.heappush(to_visit, (new_loss, new_x, new_y, d))


def calc2(data):
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # urdl

    to_visit = [(0, 0, 0, -1)]  # use a list combined with heapq instead of recursion
    visited = set()
    losses = {}

    goal = [len(data) - 1, len(data[0]) - 1]  # lower right corner
    while to_visit:
        loss, x, y, ori = heapq.heappop(to_visit)
        if x == goal[0] and y == goal[1]:
            return loss
        if (x, y, ori) in visited:
            continue
        visited.add((x, y, ori))

        for d in range(4):
            loss_inc = 0
            if d == ori or (d + 2) % 4 == ori:
                continue
            for dist in range(1, 11):
                new_x = x + dirs[d][0] * dist
                new_y = y + dirs[d][1] * dist

                if 0 <= new_x < len(data) and 0 <= new_y < len(data[0]):
                    loss_inc += data[new_x][new_y]

                    if dist < 4:
                        continue

                    new_loss = loss + loss_inc
                    group = (new_x, new_y, d)
                    if group in losses:
                        if losses[group] <= new_loss:
                            continue  # old one is better
                        losses[group] = new_loss
                    else:
                        losses[group] = new_loss

                    heapq.heappush(to_visit, (new_loss, new_x, new_y, d))
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
