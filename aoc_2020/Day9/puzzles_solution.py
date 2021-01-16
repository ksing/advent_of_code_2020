import itertools as it

from ..helper_functions import get_input_file_name, timer

PREAMBLE_SIZE = 25


def main():
    file_name = get_input_file_name(__file__)
    with open(file_name, 'r') as f:
        input_data = [int(line.strip()) for line in f]
    invalid_number = puzzle1_solution(input_data)
    print(f'Puzzle 1 solution: {invalid_number}')
    print(f'Puzzle 2 solution: {puzzle2_solution(input_data, invalid_number)}')


@timer
def puzzle1_solution(input_data):
    # https://adventofcode.com/2020/day/9

    for index, number in enumerate(input_data[PREAMBLE_SIZE:]):
        if all(
            number != sum(number_pair)
            for number_pair in it.combinations(
                input_data[index:(index + PREAMBLE_SIZE)], 2
            )
        ):
            return number
    print('Not found')


@timer
def puzzle2_solution(input_data, invalid_number):
    # https://adventofcode.com/2020/day/9#part2
    for start_index, start_number in enumerate(input_data):
        if start_number == invalid_number:
            continue
        for end_index, accumulated_sum in enumerate(it.accumulate(input_data[start_index:])):
            if accumulated_sum > invalid_number:
                # print('Sum exceeded the number already')
                continue
            if accumulated_sum == invalid_number:
                numbers_list = input_data[start_index:(start_index + end_index + 1)]
                return max(numbers_list) + min(numbers_list)


if __name__ == "__main__":
    main()
