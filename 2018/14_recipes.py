#!/usr/bin/env python3

LIMIT = 260321

def make_recipes(limit):
    recipes = [3,7]
    i_1 = 0
    i_2 = 1
    while len(recipes) < limit+10:
        new_recipe = str(recipes[i_1] + recipes[i_2])
        for digit in new_recipe:
            recipes.append(int(digit))
        i_1 = (1+i_1+recipes[i_1]) % len(recipes)
        i_2 = (1+i_2+recipes[i_2]) % len(recipes)
    return recipes[limit:limit+10]


def test_make_recipes():
    res =  make_recipes(5)
    assert ''.join([str(digit) for digit in res]) == '0124515891'
    res =  make_recipes(9)
    assert ''.join([str(digit) for digit in res]) == '5158916779'
    res =  make_recipes(18)
    assert ''.join([str(digit) for digit in res]) == '9251071085'
    res =  make_recipes(2018)
    assert ''.join([str(digit) for digit in res]) == '5941429882'


def main():
    res = make_recipes(LIMIT)
    print(''.join([str(digit) for digit in res]))
          
    
if __name__ == '__main__':
    main()
