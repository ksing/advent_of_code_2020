import re
from collections import Counter

# 1-3 s: ssss
REG = re.compile(r'(\d+)-(\d+) ([a-z]):\s+(\w+)')


def main():
    with open('./input.txt', 'r') as f:
        input_data = f.readlines()
    print(f'Puzzle 1: {sum(_is_valid_passwd_puzzle1(line.strip()) for line in input_data)}')
    print(f'Puzzle 2: {sum(_is_valid_passwd_puzzle2(line.strip()) for line in input_data)}')


def _is_valid_passwd_puzzle1(line):
    try:
        min_occur, max_occur, policy_char, passwd = REG.match(line).groups()
        return int(min_occur) <= Counter(passwd)[policy_char] <= int(max_occur)
    except AttributeError:
        return False


def _is_valid_passwd_puzzle2(line):
    try:
        min_index, max_index, policy_char, passwd = REG.match(line).groups()
        return (
            bool(passwd[int(min_index) - 1] == policy_char) !=
            bool(len(passwd) >= int(max_index) and passwd[int(max_index) - 1] == policy_char)
        )  # XOR gate implementation
    except AttributeError:
        return False


main()
