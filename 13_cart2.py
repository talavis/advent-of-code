#!/usr/bin/env python3

import sys

TURNS = {-1:0, 0:1, 1:-1}

def find_rail_type(region):
    '''
    determine type of rail in the position
    input: ltrb (left, top, right, bottom)
    '''
    rail_open = [False]*4
    for rail in enumerate(region):
        if rail[0] % 2 == 0:
            if rail[1] in '-\\/+':
                rail_open[rail[0]] = True
        else:
            if rail[1] in '|\\/+':
                rail_open[rail[0]] = True
        
    if sum(rail_open) == 4:
        return '+'
    elif rail_open[0] and rail_open[2]:
        return '-'
    elif rail_open[1] and rail_open[3]:
        return'|'
    elif rail_open[0] and rail_open[1]:
        return '/'
    elif rail_open[2] and rail_open[3]:
        return '/'
    elif rail_open[0] and rail_open[3]:
        return '\\'
    elif rail_open[2] and rail_open[1]:
        return '\\'
    return ' '


def test_find_rail_type():
    assert find_rail_type('-|-|') == '+'
    assert find_rail_type('||||') == '|'
    assert find_rail_type('----') == '-'
    assert find_rail_type('-||-') == '/'
    assert find_rail_type('+||-') == '/'
    assert find_rail_type('|--|') == '/'
    assert find_rail_type('-  |') == '\\'
    assert find_rail_type('-  |') == '\\'
    assert find_rail_type('||--') == '\\'
    assert find_rail_type('|-|-') == ' '
    assert find_rail_type('++++') == '+'


def read_railway(rawtext):
    train_chars = '<^>v'
    trains = []
    lines = rawtext.split('\n')
    coordinates = []
    trains = []
    for i in range(len(lines)):
        coordinates.append(list(lines[i]))
        for j in range(len(coordinates[i])):
            if coordinates[i][j] in train_chars:
                trains.append([i, j, train_chars.index(coordinates[i][j]), -1]) # y, x, direction (lurd), next_turn

    for train in trains:
        i = train[0]
        j = train[1]
        # makes the assumption the trains are not nejt to each other
        pos = [j-1, i-1, j+1, i+1]
        if pos[0] < 0:
            region = ' '
        else:
            region = coordinates[i][pos[0]]
        if pos[1] < 0:
            region += ' '
        else:
            region += coordinates[pos[1]][j]
        if pos[2] >= len(coordinates[i]):
            region += ' '
        else:
            region += coordinates[i][pos[2]]
        if pos[3] >= len(coordinates):
            region += ' '
        else:
            region += coordinates[pos[3]][j]

        coordinates[i][j] = find_rail_type(region)
    return coordinates, trains


def test_read_railway():
    indata = '''/->-\\        
|   |  /----\\
| /-+--+-\\  |
| | |  | v  |
\\-+-/  \\-+--/
  \\------/   '''
    coord, trains = read_railway(indata)
    assert coord == [list('/---\\        '),
                     list('|   |  /----\\'),
                     list('| /-+--+-\\  |'),
                     list('| | |  | |  |'),
                     list('\\-+-/  \\-+--/'),
                     list('  \\------/   ')]
    assert trains == [[0, 2, 2, -1], [3, 9, 3, -1]]


def tick(coordinates, trains):
    trains.sort()

    i = 0
    while i < len(trains):
        if trains[i][2] == 0:
            trains[i][1] -= 1
        if trains[i][2] == 1:
            trains[i][0] -= 1
        if trains[i][2] == 2:
            trains[i][1] += 1
        if trains[i][2] == 3:
            trains[i][0] += 1        

        train_pos = tuple((train_int[0], train_int[1]) for train_int in trains[i+1:])
        curr_pos = (trains[i][0], trains[i][1])
        if curr_pos in train_pos:
            ind_2 = train_pos.index(curr_pos)
            ind_2 += i+1
            trains.pop(ind_2)
            trains.pop(i)
            continue

        curr = coordinates[trains[i][0]][trains[i][1]]
        if trains[i][0] >= len(coordinates) or trains[i][1] >= len(coordinates[trains[i][0]]) or curr == ' ':
            sys.stderr.write(f'Problems: {trains[i]}\n')

        if curr == '+':
            trains[i][2] = (trains[i][2] + trains[i][3]) % 4
            trains[i][3] = TURNS[trains[i][3]]

        if curr == '/':
            if trains[i][2] % 2 == 0:
                trains[i][2] = (trains[i][2]-1) % 4
            else:
                trains[i][2] = (trains[i][2]+1) % 4

        if curr == '\\':
            if trains[i][2] % 2 == 1:
                trains[i][2] = (trains[i][2]-1) % 4
            else:
                trains[i][2] = (trains[i][2]+1) % 4
        i += 1
    
    # sharing position
    train_pos = tuple((train_int[0], train_int[1]) for train_int in trains)
    i = 0
    while i < len(trains):
        if train_pos.count((trains[i][0], trains[i][1])) > 1:
            ind_2 = train_pos.index((trains[i][0], trains[i][1]), i+1)
            trains.pop(ind_2)
            trains.pop(i)
        i += 1


def test_tick():
    indata = '''/>-<\\  
|   |  
| /<+-\\
| | | v
\\>+</ |
  |   ^
  \\<->/'''
    coords, trains = read_railway(indata)
    while len(trains) > 1:
        tick(coords, trains)
    tick(coords, trains)
    assert (trains[0][1], trains[0][0]) == (6, 4)


def draw_trains(coords, trains):
    tmp_coords = [coord[:] for coord in coords]
    translator = {0:'<', 1:'^', 2:'>', 3:'v'}

    for train in trains:
        tmp_coords[train[0]][train[1]] = '\033[91m' + translator[train[2]] + '\033[0m'

    rows = ['']*5
    for train in trains:
        i_1 = max((0, train[0]-2))
        i_2 = min(len(tmp_coords)-1, train[0]+2)
        j_1 = max((0, train[1]-2))
        j_2 = min(len(tmp_coords[0])-1, train[1]+2)
        
        for j, line in enumerate([''.join(coord[j_1:j_2+1]) for coord in tmp_coords[i_1:i_2+1]]):
            rows[j] += line + ' '
    for row in rows:
        print(row)
    print()

        
def main():
    input_data = open(sys.argv[1]).read()
    coords, trains = read_railway(input_data)
    train_len = len(trains)
    while len(trains) > 1:
        old_trains = [train[:] for train in trains]
        tick(coords, trains)
    print(f'{trains[0][1]},{trains[0][0]}')


if __name__ == '__main__':
    main()
