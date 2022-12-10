import requests

day = 9

def calc(data):
    hcoord = [0,0]
    tcoord = [0,0]
    passed = {(0,0)}
    changer = (0,0)
    for row in data:
        if row[0] == "R":
            changer = (1,0)
        elif row[0] == "L":
            changer = (-1,0)
        elif row[0] == "U":
            changer = (0, 1)
        elif row[0] == "D":
            changer = (0, -1)
        for _ in range(int(row[2:])):
            hcoord[0] += changer[0]
            hcoord[1] += changer[1]
            if abs(tcoord[0]-hcoord[0]) > 1 or abs(tcoord[1]-hcoord[1]) > 1:
                tcoord[0] += changer[0]
                tcoord[1] += changer[1]

                if changer[0]:
                    if hcoord[1] > tcoord[1]:
                        tcoord[1] += 1
                    elif hcoord[1] < tcoord[1]:
                        tcoord[1] -= 1
                elif changer[1]:
                    if hcoord[0] > tcoord[0]:
                        tcoord[0] += 1
                    elif hcoord[0] < tcoord[0]:
                        tcoord[0] -= 1
                passed.add(tuple(tcoord))

    return len(passed)


def check_dist(hcoord, tcoord):
    if abs(tcoord[0]-hcoord[0]) > 1:
        if hcoord[0] > tcoord[0]:
            tcoord[0] += 1
            if hcoord[1] > tcoord[1]:
                tcoord[1] += 1
            if hcoord[1] < tcoord[1]:
                tcoord[1] -= 1
        elif hcoord[0] < tcoord[0]:
            tcoord[0] -= 1
            if hcoord[1] > tcoord[1]:
                tcoord[1] += 1
            if hcoord[1] < tcoord[1]:
                tcoord[1] -= 1
    if abs(tcoord[1]-hcoord[1]) > 1:
        if hcoord[1] > tcoord[1]:
            tcoord[1] += 1
            if hcoord[0] > tcoord[0]:
                tcoord[0] += 1
            if hcoord[0] < tcoord[0]:
                tcoord[0] -= 1
        elif hcoord[1] < tcoord[1]:
            tcoord[1] -= 1
            if hcoord[0] > tcoord[0]:
                tcoord[0] += 1
            if hcoord[0] < tcoord[0]:
                tcoord[0] -= 1


def calc2(data):
    score = 0
    hcoord = [0,0]
    tail = [[0,0] for _ in range(9)]
    passed = {(0,0)}
    changer = (0,0)
    for row in data:
        if row[0] == "R":
            changer = (1,0)
        elif row[0] == "L":
            changer = (-1,0)
        elif row[0] == "U":
            changer = (0, 1)
        elif row[0] == "D":
            changer = (0, -1)
        for _ in range(int(row[2:])):
            hcoord[0] += changer[0]
            hcoord[1] += changer[1]
            change = check_dist(hcoord, tail[0])            
            for i in range(1, len(tail)):
                change = check_dist(tail[i-1], tail[i])
            passed.add(tuple(tail[8]))
    return len(passed)


def print_coord(coords, matrix_side=0, start=(0,0), rope=False):
    if matrix_side:
        matrix = [["."]*matrix_side for _ in range(matrix_side)]
        xmin = min([val[0] for val in coords])
        ymin = min([val[1] for val in coords])

    else:
        xmin = min([val[0] for val in coords])
        xmax = max([val[0] for val in coords])
        ymin = min([val[1] for val in coords])
        ymax = max([val[1] for val in coords])
        matrix = [["."]*(abs(xmin-xmax)+1) for _ in range(abs(ymin-ymax)+1)]
    if not start:
        xmod = -xmin
        ymod = -ymin
    else:
        xmod = start[0]
        ymod = start[1]

    rope_pos = "H123456789"
    for i, val in enumerate(coords):
        if rope:
            char = rope_pos[i]
        else:
            char = "#"
        if matrix[val[1]+ymod][val[0]+xmod] == '.':
            matrix[val[1]+ymod][val[0]+xmod] = char
    for row in matrix[::-1]:
        print(''.join(row))

test_data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

test_data2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

test_data = [row for row in test_data.split("\n") if row]
test_data2 = [row for row in test_data2.split("\n") if row]


res1 = calc(test_data)
res2a = calc2(test_data)
res2b = calc2(test_data2)
ans1 = 13
ans2a = 1
ans2b = 36
print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
print(f"Test part 2: {res2a} ({ans2a}){'   !!!' if res2a != ans2a else ''}")
print(f"Test part 2: {res2b} ({ans2b}){'   !!!' if res2b != ans2b else ''}")

cookies = {"session": open("cookie.dat").read()}
req = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies)
data_rows = req.text.split("\n")
data = [row for row in data_rows if row]

print(f"Part 1: {calc(data)}")
print(f"Part 2: {calc2(data)}")
