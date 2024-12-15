import requests

day = 15
part1 = True
part2 = True
testing = True
active = True

test_data = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

test_data2 = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

test_ans1 = 10092
test_ans2 = 9021


def parse(indata):
    area, instructions = indata.split("\n\n")
    area = [row for row in area.split("\n") if row]
    instructions = "".join(instructions.split("\n"))
    return (area, instructions)


def calc(data):
    area = [list(row) for row in data[0]]
    instructions = data[1]
    for i, r in enumerate(area):
        for j, c in enumerate(r):
            if c == "@":
                pos = (i, j)
                area[i][j] = "."
                break
    dirs = {"^": (-1, 0), "<": (0, -1), "v": (1, 0), ">": (0, 1)}

    for i in instructions:
        np = (pos[0] + dirs[i][0], pos[1] + dirs[i][1])
        if area[np[0]][np[1]] == ".":
            pos = np
        elif area[np[0]][np[1]] == "O":
            moves = 1
            while area[np[0] + dirs[i][0] * moves][np[1] + dirs[i][1] * moves] not in (
                ".",
                "#",
            ):
                moves += 1
            if area[np[0] + dirs[i][0] * moves][np[1] + dirs[i][1] * moves] == ".":
                for m in range(1, moves + 1):
                    area[np[0] + dirs[i][0] * m][np[1] + dirs[i][1] * m] = "O"
                area[np[0]][np[1]] = "."
                pos = np

    ans = 0
    for i, r in enumerate(area):
        for j, c in enumerate(r):
            if c == "O":
                ans += 100 * i + j
    #    for r in area:
    #        print("".join(r))
    return ans


def calc2(data):
    def print_area(area, pos=None):
        for i, r in enumerate(area):
            if pos:
                if i == pos[0]:
                    r = list(r)
                    r[pos[1]] = "@"
            print("".join(r))

    area = []
    for row in data[0]:
        area.append([])
        for c in row:
            if c == "O":
                area[-1].append("[")
                area[-1].append("]")
            else:
                area[-1].append(c)
                area[-1].append(c)
    instructions = data[1]
    for i, r in enumerate(area):
        for j, c in enumerate(r):
            if c == "@":
                pos = (i, j)
                area[i][j] = "."
                area[i][j + 1] = "."
                break
    dirs = {"^": (-1, 0), "<": (0, -1), "v": (1, 0), ">": (0, 1)}

    def move(c, i):
        if area[c[0]][c[1]] == ".":
            return True, [c], {}
        if area[c[0]][c[1]] == "#":
            return False, [], {}

        if i in ("v", "^"):
            if i == "v":
                v = 1
            elif i == "^":
                v = -1
            if area[c[0]][c[1]] == "[":
                ccoords = [(c[0], c[1]), (c[0], c[1] + 1)]
                coords = ((c[0] + v, c[1]), (c[0] + v, c[1] + 1))
            elif area[c[0]][c[1]] == "]":
                ccoords = [(c[0], c[1] - 1), (c[0], c[1])]
                coords = ((c[0] + v, c[1] - 1), (c[0] + v, c[1]))

            res1, coords1, new_data1 = move(coords[0], i)
            res2, coords2, new_data2 = move(coords[1], i)
            if res1 and res2:
                new_data = {coords[0]: "[", coords[1]: "]"}
                new_data.update(new_data1)
                new_data.update(new_data2)
                ccoords.extend(coords1)
                ccoords.extend(coords2)
                return True, ccoords, new_data
        else:
            if i == ">":
                v = 1
            elif i == "<":
                v = -1
            coord = (c[0], c[1] + v)

            res, rcoord, rnew_data = move(coord, i)
            if res:
                new_data = {coord: area[c[0]][c[1]]}
                new_data.update(rnew_data)
                return True, rcoord + [c], new_data

        return False, [], {}

    for i in instructions:
        np = (pos[0] + dirs[i][0], pos[1] + dirs[i][1])
        if area[np[0]][np[1]] == ".":
            pos = np
        elif area[np[0]][np[1]] in ("[", "]"):
            res, coords, new_data = move(np, i)
            if res:
                for c in coords:
                    area[c[0]][c[1]] = "."
                for c in new_data:
                    area[c[0]][c[1]] = new_data[c]
                pos = np

    ans = 0
    for i, r in enumerate(area):
        for j, c in enumerate(r):
            if c == "[":
                ans += 100 * i + j

    # print_area(area, pos)
    return ans


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
    with open("cookie.dat") as f:
        cookies = {"session": f.read()}
    try:
        with open(f"{day}.txt") as f:
            raw = f.read()
    except FileNotFoundError:
        raw = requests.get(f"https://adventofcode.com/2024/day/{day}/input", cookies=cookies).text
        with open(f"{day}.txt", "w") as outfile:
            outfile.write(raw)
    if part1:
        data = parse(raw)
        print(f"Part 1: {calc(data)}")
    if part2:
        data = parse(raw)
        print(f"Part 2: {calc2(data)}")
