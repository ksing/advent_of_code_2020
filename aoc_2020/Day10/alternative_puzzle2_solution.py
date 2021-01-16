import sys
from dataclasses import dataclass
from itertools import takewhile
from typing import Tuple


@dataclass
class Tree:
    start: int = 0
    entries: Tuple = (0,)
    end: int = 0


def main(file_name):
    with open(file_name, 'r') as f:
        input_data = sorted(int(line.strip()) for line in f)
    input_data.append(_get_device_joltage(input_data))
    print(f'Puzzle 2 solution: {puzzle2_solution(input_data)}')


def _get_device_joltage(input_data):
    return max(input_data) + 3


@timer
def puzzle2_solution(input_data):
    # https://adventofcode.com/2020/day/10#part2
    # Only works with small lists :(
    possibilities = _get_sequences(0, Tree(), input_data)
    # print(possibilities)
    return len(possibilities)


def _get_sequences(start_number, tree, joltage_list):
    list_trees = []
    if not joltage_list:
        return list_trees

    for index, number in enumerate(takewhile(lambda x: x - start_number <= 3, joltage_list)):
        new_tree = Tree(
            start=tree.start,
            entries=(*tree.entries, number),
            end=number
        )
        if number == joltage_list[-1]:
            print(new_tree)
            list_trees.append(new_tree)
        list_trees += _get_sequences(number, new_tree, joltage_list[index + 1:])
    return list_trees


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = './input.txt'
    main(file_name)
