import requests

day = 10
part1 = True
part2 = True
testing = True
active = True

test_data = """
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

test_data2 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

test_ans1 = 4
test_ans2 = 10


def parse(indata):
    data_rows = indata.split("\n")
    data = [row for row in data_rows if row]
    return data

# tlrb
# allows 3-d for opposite direction

o_dir = {
    "|": (1,0,0,1),
    "-": (0,1,1,0),
    "L": (1,0,1,0),
    "J": (1,1,0,0),
    "7": (0,1,0,1),
    "F": (0,0,1,1),
    ".": (0,0,0,0),
    "S": (1,1,1,1),
}

C = ((-1,0), (0,-1), (0, 1), (1, 0))

class Network:
    def __init__(self, data):
        self.pipes = []
        for i in range(len(data)):
            self.pipes.append([])
            for j in range(len(data[0])):
                self.pipes[-1].append(Pipe([i, j], data))
                if data[i][j] == "S":
                    self.start = [i,j]

    def find_loops(self):
        loops = []
        for i in range(len(C)):
            loop = [self.start]
            c = list(self.start)
            c[0] += C[i][0]
            c[1] += C[i][1]
            p = self.get_pipe(c)
            if p.open_from(self.start):
                loop.append(p.coord)
                old_p = self.get_pipe(self.start)
                while p and p.coord != self.start:
                    curr_p = p
                    p = self.get_pipe(p.next_pipe(old_p.coord))
                    old_p = curr_p
                    if p:
                        loop.append(p.coord)
            if loop[0] == loop[-1] and len(loop) > 1:
                loops.append(loop)
        return loops

    def get_pipe(self, coord):
        if coord:
            return self.pipes[coord[0]][coord[1]]

class Pipe:
    def __init__(self, coord, data):
        self.coord = coord
        self.io = o_dir[data[coord[0]][coord[1]]]
        self.allowed = []
        for i in range(len(self.io)):
            if self.io[i]:
                c = list(self.coord)
                c[0] += C[i][0]
                c[1] += C[i][1]
                if 0 <= c[0] < len(data) and 0 <= c[1] < len(data[0]):
                    self.allowed.append(c)

    def open_from(self, coord):
        if coord in self.allowed:
            return True

    def next_pipe(self, coord):
        for c in self.allowed:
            if coord != c:
                return c
        return None

        

def calc(data):
    network = Network(data)
    loops = network.find_loops()
    l = len(loops[0])-1
    score = l//2 + (l%2)
    return score


def calc2(data):
    def fill(start, blocks):
        queue = [start]
        blocks[start[0]][start[1]] = 4
        while queue:
            c = queue.pop(0)
            for d in C:
                new_c = [c[0]+d[0], c[1]+d[1]]
                if blocks[new_c[0]][new_c[1]] == 0:
                    blocks[new_c[0]][new_c[1]] = 4
                    queue.append(new_c)

    # Plot loop vertices + edges
    # mark all spots that can be reached
    # count the non-touched "potential vertices"
    network = Network(data)
    loops = network.find_loops()
    blocks = [[0]*(2*len(data[0])-1) for row in range(2*len(data)-1)]
    for i in range(len(loops[0])):
        blocks[loops[0][i][0]*2][loops[0][i][1]*2] = 1
        if i > 0:
            d = [0,0]
            d[0] = loops[0][i-1][0]-loops[0][i][0]
            d[1] = loops[0][i-1][1]-loops[0][i][1]
            c = [loops[0][i][0]*2, loops[0][i][1]*2]
            c[0] += d[0]
            c[1] += d[1]
            blocks[c[0]][c[1]] = 2

    for i in range(len(data[0])):
        if blocks[0][i] == 0:
            fill([0,i], blocks)
    for i in range(len(data[-1])):
        if blocks[-1][i] == 0:
            fill([-1,i], blocks)
    for i in range(len(data)):
        if blocks[i][0] == 0:
            fill([i,0], blocks)
        if blocks[i][-1] == 0:
            fill([i,-1], blocks)

    score = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            if blocks[i*2][j*2] == 0:
                score += 1
    return score


if testing:
    test_data_p = parse(test_data)
    test_data_p2 = parse(test_data2)

    if part1:
        res1 = calc(test_data_p)
        ans1 = test_ans1
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    if part2:
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
    data = parse(raw)
    if part1:
        print(f"Part 1: {calc(data)}")
    if part2:
        print(f"Part 2: {calc2(data)}")
