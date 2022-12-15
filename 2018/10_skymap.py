#!/usr/bin/env python3

import sys

def read_coords(rawtext):
    coords = []
    for line in rawtext.split('\n'):
        if not line:
            continue
        i = line.index('<')+1
        j = line.index(',', i)
        pos_x = int(line[i:j])
        i = j+1
        j = line.index('>', i)
        pos_y = int(line[i:j])
        i = line.index('<', j)+1
        j = line.index(',', i)
        vel_x = int(line[i:j])
        i = j+1
        j = line.index('>', i)
        vel_y = int(line[i:j])
        coords.append([pos_x, pos_y, vel_x, vel_y])
    return coords


def test_gen_skymap():
    rawtext = '''position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>'''
    coords = read_coords(rawtext)

    ref_skymap = '''........#.............
................#.....
.........#.#..#.......
......................
#..........#.#.......#
...............#......
....#.................
..#.#....#............
.......#..............
......#...............
...#...#.#...#........
....#..#..#.........#.
.......#..............
...........#..#.......
#...........#.........
...#.......#..........'''
    skymap = gen_skymap(coords)
    assert ref_skymap == skymap

    skystep(coords)
    skymap = gen_skymap(coords)
    ref_skymap = '''........#....#....
......#.....#.....
#.........#......#
..................
....#.............
..##.........#....
....#.#...........
...##.##..#.......
......#.#.........
......#...#.....#.
#...........#.....
..#.....#.#.......'''
    assert ref_skymap == skymap

    ref_skymap = '''
..........#...
#..#...####..#
..............
....#....#....
..#.#.........
...#...#......
...#..#..#.#..
#....#.#......
.#...#...##.#.
....#.........'''
    skystep(coords)
    skymap = gen_skymap(coords)


def calc_minmax(coords):
    min_x = min(coord[0] for coord in coords)
    max_x = max(coord[0] for coord in coords)
    min_y = min(coord[1] for coord in coords)
    max_y = max(coord[1] for coord in coords)
    return min_x, max_x, min_y, max_y


def gen_skymap(coords):
    min_x, max_x, min_y, max_y = calc_minmax(coords)
    x_mod = -min_x
    y_mod = -min_y
    skymap = [['.']*(max_x-min_x+1) for i in range(max_y-min_y+1)]
    for coord in coords:
        skymap[coord[1]+y_mod][coord[0]+x_mod] = '#'
    outmap = '\n'.join([''.join(row) for row in skymap])
    return outmap


def skystep(coords):
    for coord in coords:
        coord[0] += coord[2]
        coord[1] += coord[3]


def main():
    coords = read_coords(open(sys.argv[1]).read())
    lowest = float('inf')
    coord_snap = [coord for coord in coords]
    grow_i = 0
    i = 0
    best_i = 0
    while grow_i < 10:
        i += 1
        tmp = calc_minmax(coords)
        if lowest > sum(val**2 for val in tmp):
            lowest = sum(val**2 for val in tmp)
            grow_i = 0
            coord_snap = [coord[:] for coord in coords]
            best_i = i
        else:
            grow_i += 1
        skystep(coords)
    print(best_i)
    skystep(coord_snap)
    print(gen_skymap(coord_snap))


if __name__ == '__main__':
    main()
