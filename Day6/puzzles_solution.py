import re
import sys
from collections import Counter


def main(file_name):
    with open(file_name, 'r') as f:
        input_data = f.read().split('\n\n')
    print(f'Puzzle 1 solution: {puzzle1_solution(input_data)}')
    print(f'Puzzle 2 solution: {puzzle2_solution(input_data)}')


def puzzle1_solution(input_data):
    return sum(len(set(re.findall(r'[a-z]', group_responses))) for group_responses in input_data)


def puzzle2_solution(input_data):
    def _num_all_yes(group_responses):
        return len([
            question
            for question, num_yes in Counter(re.findall(r'[a-z]', group_responses)).items()
            if num_yes == len(group_responses.split('\n'))
        ])

    return sum(_num_all_yes(group.strip()) for group in input_data)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = './input.txt'
    main(file_name)
