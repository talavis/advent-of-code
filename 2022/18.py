import requests

day = 18

def parse(indata):
    data_rows = indata.split("\n")
    data = [[int(val) for val in row.split(",")] for row in data_rows if row]
    return data


class Cube:
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]
        self.connects = [None]*6
        # sides = xy lower/upper, xz lower/upper, yz lower/upper
        # [self.x == other.x, self.y == other.y
        # yz: x-1 x+1 y=y z=z
        
    def connect(self, cube):
        if self.x == cube.x and self.y == cube.y:
            if self.z == cube.z-1:
                self.connects[0] = cube
                return 0
            elif self.z == cube.z+1:
                self.connects[1] = cube
                return 1
        elif self.x == cube.x and self.z == cube.z:
            if self.y == cube.y-1:
                self.connects[2] = cube
                return 2
            elif self.y == cube.y+1:
                self.connects[3] = cube
                return 3
        elif self.y == cube.y and self.z == cube.z:
            if self.x == cube.x-1:
                self.connects[4] = cube
                return 4
            elif self.x == cube.x+1:
                self.connects[5] = cube
                return 5
        return -1

    def surface(self):
        return len(self.connects) - sum([conn is not None for conn in self.connects])

    def __repr__(self):
        connects = []
        for connect in self.connects:
            connects.append(0) if connect is None else connects.append(1)
        return f"<{self.x},{self.y},{self.z}: {connects}>"

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
        

def calc(data):
    cubes = [Cube(coord) for coord in data]
    for i in range(len(cubes)):
        for j in range(len(cubes)):
            if i == j:
                continue
            cubes[i].connect(cubes[j])

    vol = sum([cube.surface() for cube in cubes])
    return vol


def calc2(data):
    cubes = [Cube(coord) for coord in data]
    for i in range(len(cubes)):
        for j in range(len(cubes)):
            if i == j:
                continue
            cubes[i].connect(cubes[j])

    # fill in empty cubes, including external layer
    ecubes = []
    max_x = max(cubes, key=lambda c: c.x).x+1
    max_y = max(cubes, key=lambda c: c.y).y+1
    max_z = max(cubes, key=lambda c: c.z).z+1
    for x in range(max_x):
        for y in range(max_y):
            for z in range(max_z):
                coord = [x, y, z]
                if coord not in data:
                    ecubes.append(Cube(coord))

    for i in range(len(ecubes)):
        for j in range(len(ecubes)):
            if i == j:
                continue
            ecubes[i].connect(ecubes[j])

    # identify empty cubes on the outside
    outer = {ecubes[0]}
    outer_new = set(ecubes[0].connects)
    while outer_new:
        entries = list(outer_new)
        for entry in entries:
            if entry is None:
                outer_new.remove(entry)
                continue
            outer.add(entry)
            outer_new.remove(entry)
            for ent in entry.connects:
                if ent not in outer:
                    outer_new.add(ent)

    # calculate surface
    internal_vol = sum([cube.surface() for cube in ecubes if cube not in outer])
    cubes_vol = sum([cube.surface() for cube in cubes])
    return cubes_vol-internal_vol


test_data = """1,1,1
2,1,1"""

test_data2 = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

test_data = parse(test_data)
test_data2 = parse(test_data2)

testing = True
if testing:
    res1 = calc(test_data)
    res1b = calc(test_data2)
    res2 = calc2(test_data2)
    ans1 = 10
    ans1b = 64
    ans2 = 58
    print(f"Test part 1: {res1} ({ans1}){'   !!!' if res1 != ans1 else ''}")
    print(f"Test part 1b: {res1b} ({ans1b}){'   !!!' if res1b != ans1b else ''}")
    print(f"Test part 2: {res2} ({ans2}){'   !!!' if res2 != ans2 else ''}")

active = True
if active:
    cookies = {"session": open("cookie.dat").read()}
    try:
        raw = open(f"{day}.txt").read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2022/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    data = parse(raw)
    import sys
    sys.setrecursionlimit(15000)
    print(f"Part 1: {calc(data)}")
    print(f"Part 2: {calc2(data)}")
