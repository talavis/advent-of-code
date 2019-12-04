#!/usr/bin/env python3

import sys

# 5 duplicates for each digit
# 4 for 0
# 

numrange = tuple(int(val) for val in sys.argv[1].split('-'))
if numrange[0] < 10**5:
    numrange[0] = 10**5
if numrange[1] >= 10**6:
    numrange[1] = 10**6-1

amount = 0
for i in range(numrange[0], numrange[1]+1):
    number = str(i)
    dup = False
    incr = True
    for j in range(len(number)-1):
        if number[j] == number[j+1]:
            dup = True
        elif number[j] > number[j+1]:
            incr = False
    if dup and incr:
        amount += 1

print(f'Part a: {amount}')

amount = 0
for i in range(numrange[0], numrange[1]):
    number = str(i)
    dup = False
    incr = True
    for j in range(len(number)-1):
        if number[j] == number[j+1]:
            if j == 0:
                if number[j+2] != number[j]:
                    dup = True
            elif j == len(number)-2:
                if number[j-1] != number[j]:
                    dup = True
            else:
                if number[j+2] != number[j] and number[j-1] != number[j]:
                    dup = True
        elif number[j] > number[j+1]:
            incr = False
    if dup and incr:
        amount += 1

print(f'Part b: {amount}')
