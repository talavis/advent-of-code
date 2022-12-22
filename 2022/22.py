import requests

day = 22
part1 = True
part2 = True
testing = True
active = True


def parse(indata):
    board = []
    dirs = []
    div = False
    for row in indata.split("\n"):
        if not row:
            div = True
            continue
        if div:
            current = ""
            for c in row:
                if c in ("R", "L"):
                    dirs.append(int(current))
                    dirs.append(c)
                    current = ""
                else:
                    current = current + c
            dirs.append(int(current))
        else:
            board.append(list(row))
    return board, dirs


class Rotation:
    def __init__(self):
        self.dirs = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self._rot = 0

    def rotate(self, dir):
        if dir == "R":
            self._rot += 1
            if self._rot >= len(self.dirs):
                self._rot = 0
        elif dir == "L":
            self._rot -= 1
            if self._rot < 0:
                self._rot = len(self.dirs) - 1
        else:
            print("Bad dir")

    def nrotate(self, n):
        for _ in range(n):
            self.rotate("R")

    @property
    def rot(self):
        return self.dirs[self._rot]


def calc(data):
    board, dirs = data
    rot = Rotation()
    pos = [0, board[0].index(".")]

    for step in dirs:
        if step in ("R", "L"):
            rot.rotate(step)
        else:
            i = 0
            while i < step:
                i += 1
                new_pos = [pos[0] + rot.rot[0], pos[1] + rot.rot[1]]
                if 0 <= new_pos[0] < len(board) and 0 <= new_pos[1] < len(board[new_pos[0]]):
                    new_board_pos = board[new_pos[0]][new_pos[1]]
                else:
                    new_board_pos = " "
                if new_board_pos == " ":
                    tmp_pos = list(pos)
                    while board[tmp_pos[0]][tmp_pos[1]] != " ":
                        tmp_pos = [tmp_pos[0] - rot.rot[0], tmp_pos[1] - rot.rot[1]]
                        if (
                            tmp_pos[0] < 0
                            or tmp_pos[0] >= len(board)
                            or tmp_pos[1] < 0
                            or tmp_pos[1] >= len(board[tmp_pos[0]])
                        ):
                            break
                    tmp_pos = [tmp_pos[0] + rot.rot[0], tmp_pos[1] + rot.rot[1]]
                    if board[tmp_pos[0]][tmp_pos[1]] != "#":
                        pos = tmp_pos
                elif new_board_pos == ".":
                    pos = new_pos
    score = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + rot._rot

    return score


class Node:
    def __init__(self, value, coord, neighs=None):
        self.neighs = neighs  # right, down, left, up
        self.value = value
        self.coord = coord
        side = None

    def __repr__(self):
        n_out = list(self.neighs)
        for i in range(len(n_out)):
            if n_out[i] is not None:
                n_out[i] = f"v={n_out[i].value} c={n_out[i].coord}"
        return f"<v={self.value} c={self.coord} n={n_out}>"


class Grid:
    def __init__(self, board, size, test):
        local = []
        for i in range(len(board)):
            local.append(list(board[i]))
            for j in range(len(board[i])):
                local[i][j] = Node(board[i][j], (i, j), [None] * 4)

        # create connections
        for i in range(len(local)):
            for j in range(len(local[i])):
                dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
                for k, di in enumerate(dirs):
                    ni = i + di[0]
                    nj = j + di[1]
                    if 0 <= ni < len(board) and 0 <= nj < len(board[ni]):
                        node = local[ni][nj]
                        if node.value in (".", "#"):
                            local[i][j].neighs[k] = node

        # find sides (regions)
        regions = []
        self.sides = []
        for i in range(0, len(board), size):
            for j in range(0, len(board[i]), size):
                if board[i][j] in (".", "#"):
                    regions.append((i, j))
                    side = []
                    for k in range(i, i + size):
                        side += local[k][j : j + size]
                    for node in side:
                        node.side = len(regions)
                    self.sides.append(side)

        # generate edges
        edges = [[]]
        for i, reg in enumerate(regions):
            # top
            edges.append(tuple(local[reg[0]][reg[1] : reg[1] + size]))
            # left
            edges.append(tuple(row[reg[1]] for row in local[reg[0] : reg[0] + size]))
            # down
            edges.append(tuple(local[reg[0] + size - 1][reg[1] : reg[1] + size]))
            # right
            edges.append(tuple(row[reg[1] + size - 1] for row in local[reg[0] : reg[0] + size]))

        # map nodes along the edges
        # region order; sides: top, left, down, right
        if test:
            mapping = {
                1: -5,
                2: 9,
                3: 13,
                4: -24,
                5: -1,
                6: -23,
                7: -19,
                8: 10,
                9: 2,
                10: 8,
                11: -18,
                12: 14,
                13: 3,
                14: 12,
                15: 17,
                16: -21,
                17: 15,
                18: -11,
                19: -7,
                20: 22,
                21: -16,
                22: 20,
                23: -6,
                24: -4,
            }
        else:
            mapping = {
                1: 22,
                2: -14,
                3: 9,
                4: 6,
                5: 23,
                6: 4,
                7: 12,
                8: -20,
                9: 3,
                10: 13,
                11: 17,
                12: 7,
                13: 10,
                14: -2,
                15: 21,
                16: 18,
                17: 11,
                18: 16,
                19: 24,
                20: -8,
                21: 15,
                22: 1,
                23: 5,
                24: 19,
            }
        sides = [0, 3, 2, 1]
        for i, edge in enumerate(edges):
            if not edge:
                continue
            side = sides[i % 4]
            m = mapping[i]
            if m < 0:
                current = -1
                m = -m
                for j in range(len(edge)):
                    edge[j].neighs[side] = edges[m][current]
                    current -= 1
            else:
                for j in range(len(edge)):
                    edge[j].neighs[side] = edges[m][j]
                pass
        self.pos = local[0][board[0].index(".")]
        self.rot = Rotation()

        if test:
            self.migrations = {
                1: {
                    6: 2,
                    4: 0,
                    3: 3,
                    2: 2,
                },
                2: {
                    1: 2,
                    3: 0,
                    5: 2,
                    6: 1,
                },
                3: {
                    2: 0,
                    1: 1,
                    5: 3,
                    4: 0,
                },
                4: {
                    3: 0,
                    1: 0,
                    5: 0,
                    6: 1,
                },
                5: {
                    4: 0,
                    6: 0,
                    2: 2,
                    3: 1,
                },
                6: {
                    4: 3,
                    5: 0,
                    2: 3,
                    1: 2,
                },
            }
        else:
            self.migrations = {
                1: {
                    2: 0,
                    3: 0,
                    4: 2,
                    6: 1,
                },
                2: {
                    1: 0,
                    3: 1,
                    5: 2,
                    6: 0,
                },
                3: {
                    1: 0,
                    4: 3,
                    5: 0,
                    2: 3,
                },
                4: {
                    3: 1,
                    1: 2,
                    5: 0,
                    6: 0,
                },
                5: {
                    4: 0,
                    3: 0,
                    6: 1,
                    2: 2,
                },
                6: {
                    5: 3,
                    4: 0,
                    2: 0,
                    1: 3,
                },
            }

    def find_side(self, node):
        for side in self.sides:
            if node in side:
                return side

    def move(self, step):
        if step in ("R", "L"):
            self.rot.rotate(step)
        else:
            i = 0
            while i < step:
                i += 1
                new_node = self.pos.neighs[self.rot._rot]
                if new_node.value == ".":
                    if new_node.side != self.pos.side:
                        turns = self.migrations[self.pos.side][new_node.side]
                        self.rot.nrotate(turns)
                    self.pos = new_node
                else:
                    break


def calc2(data, size=50, test=False):
    board, dirs = data
    grid = Grid(board, size, test)
    for step in dirs:
        grid.move(step)
    pos = grid.pos.coord
    score = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + grid.rot._rot
    return score


test_data = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

if testing:
    test_data = parse(test_data)

    if part1:
        res1 = calc(test_data)
        ans1 = 6032
        print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    if part2:
        res2 = calc2(test_data, 4, True)
        ans2 = 5031
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
