import re
import sys
from collections import deque
from itertools import zip_longest

SEAT_REG = re.compile(r'(?P<row_ops>[BF]{7})(?P<col_ops>[LR]{3})')
LIST_ROWS = list(range(128))
LIST_COLUMNS = list(range(8))


def main(file_name):
    with open(file_name, 'r') as f:
        input_data = sorted(_get_seat_id(line.strip()) for line in f)
    print(f'Puzzle 1 solution: {puzzle1_solution(input_data)}')
    print(f'Puzzle 2 solution: {puzzle2_solution(input_data)}')


def puzzle1_solution(seat_ids):
    return seat_ids[-1]


def puzzle2_solution(seat_ids):
    for ideal_num, seat_id in zip_longest(range(seat_ids[0], seat_ids[-1]), seat_ids):
        if seat_id != ideal_num:
            return ideal_num


def _get_seat_id(boarding_pass):
    row_ops, col_ops = SEAT_REG.match(boarding_pass).groups()
    seat_row = _binary_search(LIST_ROWS, deque(row_ops))
    seat_column = _binary_search(LIST_COLUMNS, deque(col_ops))
    seat_id = seat_row * 8 + seat_column
    # print(f'Operations: {boarding_pass}, Seat row: {seat_row}, Seat column: {seat_column}, Seat ID: {seat_id}')
    return seat_id


def _binary_search(input_list, ops_list):
    list_length = len(input_list)
    if not list_length:
        raise RecursionError("Something went wrong!")
    if list_length == 1 or not ops_list:
        return input_list[0]
    operation = ops_list.popleft()
    if operation in ('F', 'L'):
        return _binary_search(input_list[:int(list_length / 2)], ops_list)
    elif operation in ('B', 'R'):
        return _binary_search(input_list[int(list_length / 2):], ops_list)
    else:
        return _binary_search(input_list, ops_list)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = './input.txt'
    main(file_name)
