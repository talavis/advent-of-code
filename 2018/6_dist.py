#!/usr/bin/env python3

import collections
import sys


def find_shortest_dist(goal, coords):
    best_dist = (float('inf'))
    best_coord = []
    for coord in coords:
        dist = abs(coord[0]-goal[0]) + abs(coord[1]-goal[1])
        if dist < best_dist:
            best_dist = dist
            best_coord = [coord]
        elif dist == best_dist:
            best_coord.append(coord)
    return best_coord


def find_edges(board):
    edges = set()
    edges.add('.')

    for col in board[0]:
        edges.add(str(col))
    for col in board[-1]:
        edges.add(str(col))
    for row in board[1:-1]:
        edges.add(str(row[0]))
        edges.add(str(row[-1]))
    return edges


def test_dist():
    coords = [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]

    assert calc_max_area(coords) == 17


def calc_max_area(coords):
    coords.sort()
    board_max = (max(i[0] for i in coords), max(i[1] for i in coords))
    board = [[0]*(board_max[0]+1) for i in range(board_max[1]+1)]
    for i in range(len(board)):
        for j in range(len(board[0])):
            tmp = find_shortest_dist((j, i), coords)
            if len(tmp) == 1:
                board[i][j] = tmp
            else:
                board[i][j] = '.'
    flattened = [str(i) for sub in board for i in sub]
    counter = collections.Counter(flattened)
    edges = find_edges(board)
    for edge in edges:
        counter[edge] = 0
    return max(counter.values())


def main():
    coords = [(int(val[:val.index(',')]), int(val[val.index(',')+1:])) for val in open(sys.argv[1]).read().split('\n') if val]
    print(calc_max_area(coords))

if __name__ == '__main__':
    main()
