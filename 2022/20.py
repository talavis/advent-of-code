import requests

day = 20
part1 = True
part2 = True
testing = True
active = True


def parse(indata):
    data_rows = indata.split("\n")
    data = [int(row.strip()) for row in data_rows if row]
    return data


class Node:
    def __init__(self, value, shift, i, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.shift = shift
        self.i = i

    def move(self):
        self.right.left = self.left
        self.left.right = self.right
        pos = self.right
        for i in range(self.shift):
            pos = pos.right
        pos.left.right = self
        self.left = pos.left
        self.right = pos
        pos.left = self

    def find(self, target):
        node = self
        while node.i != target:
            node = node.right
            if node == self:
                return None
        return node

    def __repr__(self):
        return f"<Node: v={self.value} i={self.i}>"

    
def print_loop(current):
    start = current
    nodes = [current]
    current = current.right
    while current is not start:
        nodes.append(current)
        current = current.right
    nodes.append(current)
    print(nodes)
    start = current
    lnodes = [current]
    current = current.left
    while current is not start:
        lnodes.append(current)
        current = current.left
    lnodes.append(current)
    print(lnodes)


def create_circle(data, key=1):
    start = current = last = None
    for i, val in enumerate(data):
        last = current
        new_val = val*key
        shift = new_val % (len(data)-1)
        current = Node(new_val, shift, i, last)
        if last is not None:
            last.right = current
        if start is None:
            start = current
    current.right = start
    start.left = current
    return start
    
    
def calc(data):
    nodes = []

    current = create_circle(data)
    
    for i in range(len(data)):
        current = current.find(i)
        current.move()

    current = current.find(data.index(0))
    score = 0
    for i in range(1, 3001):
        current=current.right
        if i % 1000 == 0:
            score += current.value

    return score


def calc2(data):
    nodes = []
    key = 811589153
    current = create_circle(data, key)
    
    for _ in range(10):
        for i in range(len(data)):
            current = current.find(i)
            current.move()

    current = current.find(data.index(0))
    score = 0
    for i in range(1, 3001):
        current=current.right
        if i % 1000 == 0:
            score += current.value

    return score

test_data = """1
2
-3
3
-2
0
4"""

if testing:
    test_data = parse(test_data)

    if part1:
        res1 = calc(test_data)
        ans1 = 3
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    if part2:
        res2 = calc2(test_data)
        ans2 = 1623178306
        print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

if active:
    cookies = {"session": open("cookie.dat").read()}
    try:
        raw = open(f"{day}.txt").read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    data = parse(raw)
    if part1:
        print(f"Part 1: {calc(data)}")
    if part2:
        print(f"Part 2: {calc2(data)}")
