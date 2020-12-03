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
    match = REG.match(line)
    if match:
        min_occur, max_occur, policy_char, passwd = match.groups()
        c = Counter(passwd)
        return int(min_occur) <= c[policy_char] <= int(max_occur)
    else:
        return False


def _is_valid_passwd_puzzle2(line):
    match = REG.match(line)
    if match:
        min_occur, max_occur, policy_char, passwd = match.groups()
        return sum([
            passwd[int(min_occur) - 1] == policy_char,
            len(passwd) >= int(max_occur) and passwd[int(max_occur) - 1] == policy_char
        ]) == 1
    else:
        return False


main()
