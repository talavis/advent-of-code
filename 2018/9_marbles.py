#!/usr/bin/env python3

import sys

def test_marble():
    assert marble_func(9, 25) == 32
    assert marble_func(10, 1618) == 8317
    assert marble_func(13, 7999) == 146373
    assert marble_func(17, 1104) == 2764
    assert marble_func(21, 6111) == 54718
    assert marble_func(30, 5807) == 37305


def marble_func(nr_players, last_marble):
    marbles = [0,1]
    curr_player = 2
    players = [0]*nr_players
    curr = 1
    i = 2
    while i <= last_marble:
        if i % 23 != 0:
            curr = ((curr+1) % len(marbles))+1
            marbles.insert(curr, i)
        else:
            curr = ((curr-8) % len(marbles))+1
            tmp = marbles.pop(curr)
            players[curr_player] += i + tmp
            
        i += 1
        curr_player = (curr_player+1) % nr_players
    return max(players)


def main():
    players = 459
    last_marble = 71790
    print(marble_func(players, last_marble))

    
if __name__ == '__main__':
    main()
