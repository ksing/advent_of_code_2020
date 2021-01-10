import itertools as it
import operator as op
from functools import reduce

from ..helper_functions import get_input_file_name, timer


def main():
    file_name = get_input_file_name(__file__)
    with open(file_name, 'r') as f:
        input_data = [int(line.strip()) for line in f if line]
    print(f'Puzzle 1 solution: {_get_puzzle_solution(input_data, 2)}')
    print(f'Puzzle 2 solution: {_get_puzzle_solution(input_data, 3)}')


@timer
def _get_puzzle_solution(input_data, num_combinations):
    for numbers in it.combinations(input_data, num_combinations):
        if sum(numbers) == 2020:
            return reduce(op.mul, numbers)


main()
