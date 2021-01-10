import sys

from ..helper_functions import timer


def main(starting_numbers):
    input_data = [int(num) for num in starting_numbers.split(',')]
    print(input_data)
    print(f'Puzzle 1 solution: {puzzle_solution(input_data, 2020)}')
    print(f'Puzzle 2 solution: {puzzle_solution(input_data, 30000000)}')


@timer
def puzzle_solution(input_data, last_index):
    # https://adventofcode.com/2020/day/15
    # https://adventofcode.com/2020/day/15#part2
    number_index_dict = {number: index for index, number in enumerate(input_data)}
    next_number = 0
    for i in range(len(input_data), last_index - 1):
        # print(number_index_dict)
        # print(i, next_number)
        if next_number in number_index_dict:
            last_number, next_number = next_number, i - number_index_dict[next_number]
        else:
            last_number, next_number = next_number, 0
        number_index_dict[last_number] = i
    return next_number


if __name__ == "__main__":
    starting_numbers = sys.argv[1]
    main(starting_numbers)
