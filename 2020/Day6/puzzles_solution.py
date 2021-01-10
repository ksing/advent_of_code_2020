import re
from collections import Counter

from ..helper_functions import get_input_file_name, timer


def main():
    file_name = get_input_file_name(__file__)
    with open(file_name, 'r') as f:
        input_data = f.read().split('\n\n')
    print(f'Puzzle 1 solution: {puzzle1_solution(input_data)}')
    print(f'Puzzle 2 solution: {puzzle2_solution(input_data)}')


@timer
def puzzle1_solution(input_data):
    return sum(len(set(re.findall(r'[a-z]', group_responses))) for group_responses in input_data)


@timer
def puzzle2_solution(input_data):
    def _num_all_yes(group_responses):
        return len([
            question
            for question, num_yes in Counter(re.findall(r'[a-z]', group_responses)).items()
            if num_yes == len(group_responses.split('\n'))
        ])

    return sum(_num_all_yes(group.strip()) for group in input_data)


if __name__ == "__main__":
    main()
