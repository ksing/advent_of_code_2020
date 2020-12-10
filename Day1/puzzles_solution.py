import itertools as it
import operator as op
from functools import reduce


def main():
    with open('./input.txt', 'r') as f:
        input_data = [int(line.strip()) for line in f if line]
    print(f'Puzzle 1 solution: {_get_puzzle_solution(input_data, 2)}')
    print(f'Puzzle 2 solution: {_get_puzzle_solution(input_data, 3)}')


def _get_puzzle_solution(input_data, num_combinations):
    for numbers in it.combinations(input_data, num_combinations):
        if sum(numbers) == 2020:
            return reduce(op.mul, numbers)


main()
