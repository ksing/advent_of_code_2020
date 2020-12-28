import re
import sys
from collections import Counter
from itertools import chain
from pathlib import Path
from time import perf_counter

ALLERGEN_REG = re.compile(r'contains ([a-z]+\s)+(?:\(|$)')


def main(file_name):
    t0 = perf_counter()
    ingredient_counter, allergen_ingredient_dict = _process_allergens_ingredients(file_name)
    print(f'Time taken by in processing food data = {perf_counter() - t0}')
    print(f'Puzzle 1 solution: {puzzle1_solution(ingredient_counter, allergen_ingredient_dict)}')
    print(f'Puzzle 2 solution: {puzzle2_solution(allergen_ingredient_dict)}')


def read_file(file_name):
    with open(file_name, 'r') as f:
        for line in f:
            yield line.strip().split(' (')


def _process_allergens_ingredients(file_name):
    allergen_ingredient_dict = {}
    ingredient_counter = Counter()
    for ingredients, allergens in read_file(file_name):
        set_ingredients = set(ingredients.split())
        ingredient_counter.update(set_ingredients)
        for allergen in re.match(r'contains ([a-z ,]+)\)', allergens).group(1).split(','):
            allergen_ingredient_dict[allergen.strip()] = (
                set_ingredients
                & allergen_ingredient_dict.setdefault(allergen.strip(), set_ingredients)
            )

    print(sorted(allergen_ingredient_dict.items()))
    allergen_ingredient_dict = _reduce_allergen_ingredient_dict(allergen_ingredient_dict)
    print(sorted(allergen_ingredient_dict.items()))
    return ingredient_counter, allergen_ingredient_dict


def _reduce_allergen_ingredient_dict(allergen_ingredient_dict):
    # Recursively and step-by-step, remove ingredients from allergen list, starting from the allergen with least number
    #  of ingedients potentially associated with it.
    seen = set()
    flag = 0
    for allergen, set_ingredients in sorted(
        allergen_ingredient_dict.items(), key=lambda x: len(x[1])
    ):
        # print(allergen, set_ingredients)
        unseen_ingredients = set_ingredients - seen
        if len(unseen_ingredients) > 1:
            flag = 1
        elif len(unseen_ingredients) == 1:
            allergen_ingredient_dict[allergen] = unseen_ingredients
            seen |= allergen_ingredient_dict[allergen]
    # print(sorted(allergen_ingredient_dict.items()))
    if not flag:
        return allergen_ingredient_dict
    else:
        return _reduce_allergen_ingredient_dict(allergen_ingredient_dict)


def puzzle1_solution(ingredient_counter, allergen_ingredient_dict):
    # https://adventofcode.com/2020/day/21
    non_allergens = set(ingredient_counter) - set(chain.from_iterable(allergen_ingredient_dict.values()))
    # print(non_allergens)
    return sum(
        num_occurs for ingredient, num_occurs in ingredient_counter.items()
        if ingredient in non_allergens
    )


def puzzle2_solution(allergen_ingredient_dict):
    return ','.join(list(chain.from_iterable(
        ingredients for allergen, ingredients in sorted(allergen_ingredient_dict.items())
    )))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = Path(__file__).parent.resolve() / 'input.txt'  # type: ignore
    main(file_name)
