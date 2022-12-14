import requests

day = 14

def calc(data):
    vectors = []
    x_max, y_max = 0, 0
    for row in data:
        rvectors = [[int(v) for v in val.split(",")] for val in row.split(" -> ")]
        vectors.append(rvectors)
        y = max(rvectors, key=lambda x: x[0])[0]
        x = max(rvectors, key=lambda y: y[1])[1]     
        if y_max < y:
            y_max = y
        if x_max < x:
            x_max = x
    matrix = [["."]*(y_max+1) for _ in range(x_max+2)]
    for vec in vectors:
        for i in range(1, len(vec)):
            x_start = min(vec[i-1][1], vec[i][1])
            x_end = max(vec[i-1][1], vec[i][1])+1
            for x in range(x_start, x_end):
                matrix[x][vec[i][0]] = "#"
            y_start = min(vec[i-1][0], vec[i][0])
            y_end = max(vec[i-1][0], vec[i][0])+1
            for y in range(y_start, y_end):
                matrix[vec[i][1]][y] = "#"

    # sand
    n_sand = 0
    while True:
        y = 500
        stopped = False
        for x in range(len(matrix)-1):
            if matrix[x+1][y] != ".":
                if matrix[x+1][y-1] != ".":
                    if matrix[x+1][y+1] != ".":
                        matrix[x][y] = "o"
                        n_sand += 1
                        stopped = True
                        break
                    else:
                        y += 1
                        if y < len(matrix[0]):
                            continue
                        else:
                            break
                else:
                    y -= 1
                    if y >= 0:
                        continue
                    else:
                        break
        if not stopped:
            break

    # for row in matrix:
    #     out = ''.join(row[490:])
    #     print(out)
        
    return n_sand


def calc2(data):
    vectors = []
    x_max, y_max = 0, 0
    for row in data:
        rvectors = [[int(v) for v in val.split(",")] for val in row.split(" -> ")]
        vectors.append(rvectors)
        y = max(rvectors, key=lambda x: x[0])[0]
        x = max(rvectors, key=lambda y: y[1])[1]     
        if y_max < y:
            y_max = y
        if x_max < x:
            x_max = x
    matrix = [["."]*(y_max*2) for _ in range(x_max+2)]
    matrix.append(["#"]*(y_max*2))
    for vec in vectors:
        for i in range(1, len(vec)):
            x_start = min(vec[i-1][1], vec[i][1])
            x_end = max(vec[i-1][1], vec[i][1])+1
            for x in range(x_start, x_end):
                matrix[x][vec[i][0]] = "#"
            y_start = min(vec[i-1][0], vec[i][0])
            y_end = max(vec[i-1][0], vec[i][0])+1
            for y in range(y_start, y_end):
                matrix[vec[i][1]][y] = "#"
        
    # sand
    n_sand = 0
    done = False
    while not done:
        y = 500
        for x in range(len(matrix)-1):
            if matrix[x+1][y] != ".":
                if matrix[x+1][y-1] != ".":
                    if matrix[x+1][y+1] != ".":
                        matrix[x][y] = "o"
                        n_sand += 1
                        if x == 0 and y == 500:
                            done = True
                        break
                    else:
                        y += 1
                        if y < len(matrix[0]):
                            continue
                        else:
                            print(f"{y=}")
                            break
                else:
                    y -= 1
                    if y >= 0:
                        continue
                    else:
                        print(f"{y=}")
                        break

    # for row in matrix:
    #     out = ''.join(row[480:520])
    #     print(out)
        
    return n_sand


test_data = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

test_data = [row for row in test_data.split("\n") if row]


res1 = calc(test_data)
res2 = calc2(test_data)
ans1 = 24
ans2 = 93
print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

cookies = {"session": open("cookie.dat").read()}
req = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies).text
data_rows = req.split("\n")
#data_rows = open(f"{day}.txt".split("\n")
data = [row for row in data_rows if row]

print(f"Part 1: {calc(data)}")
print(f"Part 2: {calc2(data)}")
