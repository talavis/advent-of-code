import requests

import sys

sys.setrecursionlimit(40000)

day = 12

INACTIVE = -3
ACTIVE = -1
FAIL = -2

LETTERS = "SabcdefghijklmnopqrstuvwxyzE"


class Node:
    def __init__(self, value, neighbours=None):
        if neighbours is None:
            neighbours = []
        self.dist = float("inf")
        self.prev = None
        self.visited = False
        self.value = value
        self.neighbours = neighbours

    def __repr__(self):
        return f"<Node: .value: {self.value} .dist: {self.dist}>"

    def update_neighbours(self):
        for neigh in self.neighbours:
            if neigh.value - self.value >= -1:
                if self.dist + 1 < neigh.dist:
                    neigh.dist = self.dist + 1
                    neigh.prev = self
        self.visited = True


class Container:
    def __init__(self, indata):
        self.nodes = []
        nodes = []
        for row in indata:
            nodes.append([Node(LETTERS.index(c)) for c in row])
            if "S" in row:
                self.s = nodes[-1][row.index("S")]
            if "E" in row:
                self.e = nodes[-1][row.index("E")]
                self.e.dist = 0
        for i, row in enumerate(nodes):
            for j, node in enumerate(row):
                node.neighbours = []
                if i > 0:
                    node.neighbours.append(nodes[i - 1][j])
                if i < len(nodes) - 1:
                    node.neighbours.append(nodes[i + 1][j])
                if j > 0:
                    node.neighbours.append(nodes[i][j - 1])
                if j < len(nodes[i]) - 1:
                    node.neighbours.append(nodes[i][j + 1])
            self.nodes += row

    def next_node(self):
        nodes = [node for node in self.nodes if not node.visited]
        if nodes:
            ret = min(nodes, key=lambda x: x.dist)
        else:
            ret = None
        return ret

    def get_dist(self):
        while node := self.next_node():
            node.update_neighbours()
        return self.s.dist

    def shortest_climb(self):
        while node := self.next_node():
            node.update_neighbours()
        a_nodes = [node for node in self.nodes if node.value == LETTERS.index("a")]
        return min(a_nodes, key=lambda x: x.dist).dist


def calc(data):
    container = Container(data)
    dist = container.get_dist()
    return dist


def calc2(data):
    container = Container(data)
    dist = container.shortest_climb()
    return dist


test_data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

test_data = [row for row in test_data.split("\n") if row]


res1 = calc(test_data)
res2 = calc2(test_data)
ans1 = 31
ans2 = -1
print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

cookies = {"session": open("cookie.dat").read()}
req = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies).text
data_rows = req.split("\n")
data = [row for row in data_rows if row]

print(f"Part 1: {calc(data)}")
print(f"Part 2: {calc2(data)}")
