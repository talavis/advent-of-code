#!/usr/bin/env python3

LIMIT = 260321

def find_recipes(limit):
    limit = str(limit)
    len_limit = len(limit)+1 # to handle additions of two recipes
    scores = '37'
    i_1 = 0
    i_2 = 1
    i = 0
    while limit not in scores[-len_limit:]:
        scores += str(int(scores[i_1]) + int(scores[i_2]))
        i_1 = (1+i_1+int(scores[i_1])) % len(scores)
        i_2 = (1+i_2+int(scores[i_2])) % len(scores)
    return scores.index(limit)


def test_score_recipes():
    assert find_recipes('01245') == 5
    assert find_recipes(51589) == 9
    assert find_recipes(92510) == 18
    assert find_recipes(59414) == 2018


def main():
    print(find_recipes(LIMIT))
          
    
if __name__ == '__main__':
    main()
