import requests

day = 8

def calc(data):
    for i in range(len(data)):
        data[i] = [int(dat) for dat in data[i]]
    matrix = [[0]*len(data[0]) for _ in range(len(data))]
    matrix[0] = [1]*len(data)
    matrix[-1] = [1]*len(data)
    score = len(data)*2+len(data[0])*2-4
    for i in range(1, len(data)-1):
        matrix[i][0] = 1
        matrix[i][-1] = 1
    # right
    for i in range(1, len(data)-1):
        tallest = data[i][0]
        for j in range(1, len(data[0])-1):
            if tallest < data[i][j]:
                matrix[i][j] = 1
                tallest = data[i][j]
            if tallest == 9:
                break
    # left
    for i in range(1, len(data)-1):
        tallest = data[i][-1]
        for j in range(len(data[0])-2, 0, -1):
            if tallest < data[i][j]:
                matrix[i][j] = 1
                tallest = data[i][j]
            if tallest == 9:
                break
    # down
    for j in range(1, len(data)-1):
        tallest = data[0][j]
        for i in range(1, len(data)-1):
            if tallest < data[i][j]:
                matrix[i][j] = 1
                tallest = data[i][j]
            if tallest == 9:
                break
    # down
    for j in range(1, len(data)-1):
        tallest = data[-1][j]
        for i in range(len(data)-2, 0, -1):
            if tallest < data[i][j]:
                matrix[i][j] = 1
                tallest = data[i][j]
            if tallest == 9:
                break

    score = sum([sum(row) for row in matrix])

    return score


def calc2(data):
    for i in range(len(data)):
        data[i] = [int(dat) for dat in data[i]]
    best = 0
    for i in range(1, len(data)-1):
        for j in range(1, len(data[0])-1):
            tmp = 1
            a = i
            while a > 0:
                a -= 1
                if data[a][j] >= data[i][j]:
                    break
            tmp *= (i-a)

            a = i
            while a < len(data)-1:
                a += 1
                if data[a][j] >= data[i][j]:
                    break
            tmp *= (a-i)
            
            a = j
            while a > 0:
                a -= 1
                if data[i][a] >= data[i][j]:
                    break
            tmp *= (j-a)
                    
            a = j
            while a < len(data[0])-1:
                a += 1
                if data[i][a] >= data[i][j]:
                    break
            tmp *= (a-j)

            if tmp > best:
                best = tmp
    return best


test_data = """30373
25512
65332
33549
35390"""

test_data = [row for row in test_data.split("\n") if row]


res1 = calc(test_data)
res2 = calc2(test_data)
ans1 = 21
ans2 = 8
print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

cookies = {"session": open("cookie.dat").read()}
req = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies)
data_rows = req.text.split("\n")
data = [row for row in data_rows if row]

print(f"Part 1: {calc(data)}")
print(f"Part 2: {calc2(data)}")
