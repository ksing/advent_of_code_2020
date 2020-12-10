import sys
from collections import Counter
# from dataclasses import dataclass, field
from functools import lru_cache
from itertools import takewhile
# from typing import Tuple

# @dataclass
# class Tree:
#     start: int = 0
#     entries: Tuple = (0,)
#     end: int = 0


def main(file_name):
    with open(file_name, 'r') as f:
        input_data = sorted(int(line.strip()) for line in f)
    input_data.append(_get_device_joltage(input_data))
    print(f'Puzzle 1 solution: {puzzle1_solution(input_data)}')
    print(f'Puzzle 2 solution: {puzzle2_solution(input_data)}')


def _get_device_joltage(input_data):
    return max(input_data) + 3


def puzzle1_solution(input_data):
    # https://adventofcode.com/2020/day/10
    jolt_distribution = Counter(a-b for a, b in zip(input_data, [0] + input_data[:-1]))
    print(jolt_distribution)
    return jolt_distribution[3] * jolt_distribution[1]


def puzzle2_solution(input_data):
    # https://adventofcode.com/2020/day/10#part2
    # possibilities = _get_sequences(0, Tree(), tuple(input_data))
    # print(possibilities)
    # return len(possibilities)
    num_possibilities = _get_num_possibilities(0, tuple(input_data))
    return num_possibilities


# def _get_sequences(start_number, tree, joltage_list):
#     # Only works with small lists :(
#     list_trees = []
#     if not joltage_list:
#         return list_trees

#     for index, number in enumerate(takewhile(lambda x: x - start_number <= 3, joltage_list)):
#         new_tree = Tree(
#             start=tree.start,
#             entries=(*tree.entries, number),
#             end=number
#         )
#         if number == joltage_list[-1]:
#             # print(new_tree)
#             list_trees.append(new_tree)
#         list_trees += _get_sequences(number, new_tree, joltage_list[index + 1:])
#     return list_trees


@lru_cache(maxsize=512)
def _get_num_possibilities(start_number, joltage_list):
    num_possibilities = 0
    if not joltage_list:
        return num_possibilities

    for index, number in enumerate(takewhile(lambda x: x - start_number <= 3, joltage_list)):
        if number == joltage_list[-1]:
            # print(start_number)
            num_possibilities += 1
        num_possibilities += _get_num_possibilities(number, joltage_list[index + 1:])
    return num_possibilities


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = './input.txt'
    main(file_name)
