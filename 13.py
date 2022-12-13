import json

import requests

day = 13

# used as a wrapper to make it possible to use sort()
class Value:
    def __init__(self,value):
        self._value = value
    def __lt__(self, right):
        return compare(self._value, right._value)
    def __gt__(self, right):
        return compare(right._value, self._value)
    def __eq__(self, right):
        return self._value == right
    def __repr__(self) -> str:
        return f"{self._value}"


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    for lsub, rsub in zip(left, right):
        sub = compare(lsub, rsub)
        if sub is not None:
            return sub
    if len(left) < len(right):
        return True
    if len(left) > len(right):
        return False

    return None
            

def calc(data):
    score = 0
    for i in range(0, len(data), 2):
        dat1 = json.loads(data[i])
        dat2 = json.loads(data[i+1])
        res = compare(dat1, dat2)
        if res:
            score += i//2+1
    return score


def calc2(data):
    loaded = [Value(json.loads(row)) for row in data]
    decode1 = Value([[2]])
    decode2 = Value([[6]])
    loaded += [decode1, decode2]
    loaded.sort()
    return (loaded.index(decode1)+1)*(loaded.index(decode2)+1)


test_data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

test_data = [row for row in test_data.split("\n") if row]


res1 = calc(test_data)
res2 = calc2(test_data)
ans1 = 13
ans2 = 140
print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

cookies = {"session": open("cookie.dat").read()}
req = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies)
data_rows = req.text.split("\n")
data = [row for row in data_rows if row]

print(f"Part 1: {calc(data)}")
print(f"Part 2: {calc2(data)}")
