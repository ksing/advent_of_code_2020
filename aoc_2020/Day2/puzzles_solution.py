import re
from collections import Counter

from ..helper_functions import get_input_file_name, timer

# 1-3 s: ssss
REG = re.compile(r'(\d+)-(\d+) ([a-z]):\s+(\w+)')


def main():
    file_name = get_input_file_name(__file__)
    with open(file_name, 'r') as f:
        input_data = f.readlines()
    print(f'Puzzle 1: {puzzle1_solution(input_data)}')
    print(f'Puzzle 2: {puzzle2_solution(input_data)}')


@timer
def puzzle1_solution(input_data):
    def _is_valid_passwd(line):
        try:
            min_occur, max_occur, policy_char, passwd = REG.match(line).groups()
            return int(min_occur) <= Counter(passwd)[policy_char] <= int(max_occur)
        except AttributeError:
            return False
    return sum(_is_valid_passwd(line.strip()) for line in input_data)


@timer
def puzzle2_solution(input_data):
    def _is_valid_passwd(line):
        try:
            min_index, max_index, policy_char, passwd = REG.match(line).groups()
            return (
                bool(passwd[int(min_index) - 1] == policy_char) !=
                bool(len(passwd) >= int(max_index) and passwd[int(max_index) - 1] == policy_char)
            )  # XOR gate implementation
        except AttributeError:
            return False
    return sum(_is_valid_passwd(line.strip()) for line in input_data)


main()
