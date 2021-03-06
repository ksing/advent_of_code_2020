from collections import Counter
from functools import lru_cache
from itertools import takewhile

from ..helper_functions import get_input_file_name, timer


def main():
    file_name = get_input_file_name(__file__)
    with open(file_name, 'r') as f:
        input_data = sorted(int(line.strip()) for line in f)
    input_data.append(_get_device_joltage(input_data))
    print(f'Puzzle 1 solution: {puzzle1_solution(input_data)}')
    print(f'Puzzle 2 solution: {puzzle2_solution(input_data)}')


def _get_device_joltage(input_data):
    return max(input_data) + 3


@timer
def puzzle1_solution(input_data):
    # https://adventofcode.com/2020/day/10
    jolt_distribution = Counter(a-b for a, b in zip(input_data, [0] + input_data[:-1]))
    print(jolt_distribution)
    return jolt_distribution[3] * jolt_distribution[1]


@timer
def puzzle2_solution(input_data):
    # https://adventofcode.com/2020/day/10#part2
    num_possibilities = _get_num_possibilities(0, tuple(input_data))
    return num_possibilities


@lru_cache(maxsize=512)
def _get_num_possibilities(start_number, joltage_list):
    num_possibilities = 0
    if not joltage_list:
        return num_possibilities

    for index, number in enumerate(takewhile(lambda x: x - start_number <= 3, joltage_list)):
        if number == joltage_list[-1]:
            num_possibilities += 1
        num_possibilities += _get_num_possibilities(number, joltage_list[index + 1:])
    return num_possibilities


if __name__ == "__main__":
    main()
