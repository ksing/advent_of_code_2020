import operator as op
import sys
from functools import reduce
from pathlib import Path

import numpy as np

START = (0, 0)


def main(file_name):
    with open(file_name, 'r') as f:
        input_data = np.array(
            [
                list(line.strip().replace('.', '0').replace('#', '1'))  # Replace trees with 1
                for line in f
            ],
            dtype=int
        )
    print(f'Puzzle 1 solution: {puzzle1_solution(input_data)} trees')
    print(f'Puzzle 2 solution: {puzzle2_solution(input_data)}')


def puzzle1_solution(input_data):
    return get_number_trees_encountered(input_data, (1, 3))


def puzzle2_solution(input_data):
    steps = (
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1),
    )
    return reduce(op.mul, [get_number_trees_encountered(input_data, step) for step in steps])


def get_number_trees_encountered(data, step):
    # Broadcast the matrix so as to have the number of steps that will be taken to reach the last row
    data = np.tile(
        data,
        (1, int(np.ceil(data.shape[0] / data.shape[1]) * (step[1] // step[0] + 1)))
    )
    # Sum over all the 1's (Trees) encountered at the indices that the steps bring us to.
    return sum(
        data[START[0] + step[0] * i][START[1] + step[1] * i]
        for i in range(int(np.ceil(data.shape[0] / step[0])))
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = Path(__file__).parent.resolve() / 'input.txt'
    main(file_name)

