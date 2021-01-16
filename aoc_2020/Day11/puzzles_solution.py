import numpy as np
from numba import njit

from ..helper_functions import get_input_file_name, timer

EMPTY_SEAT = 0
OCCUPIED_SEAT = 1
FLOOR = 2


def main():
    file_name = get_input_file_name(__file__)
    with open(file_name, 'r') as f:
        input_data = [
            list(line.replace('L', '0').replace('#', '1').replace('.', '2').strip())
            for line in f
        ]
    print(f'Puzzle 1 solution: {puzzle1_solution(np.array(input_data, dtype=np.int8))}')
    print(f'Puzzle 2 solution: {puzzle2_solution(np.array(input_data, dtype=np.int8))}')


@njit
def _get_num_occupied_adjacent_seats(seat_matrix):
    return (seat_matrix == OCCUPIED_SEAT).sum()


@njit
def _get_seat_changes(seat, adjacent_seats):
    # In puzzle 1, the adjacent seats are defined as the 3-8 seats surrounding it.
    # In puzzle 2, the adjacent seats are defined by the first visible seat in each direction.
    # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    # In puzzle 1: If a seat is occupied (#) and four or more seats adjacent to it are also occupied,
    #  the seat becomes empty.
    # In puzzle 2: If that number is 5 or more, seat becomes empty.
    # Otherwise, the seat's state does not change.
    if seat == EMPTY_SEAT and _get_num_occupied_adjacent_seats(adjacent_seats) == 0:
        return OCCUPIED_SEAT
    elif seat == OCCUPIED_SEAT and _get_num_occupied_adjacent_seats(adjacent_seats) > 4:
        # It works in both puzzles, because in puzzle 1's adjacent seat matrix, seat at (1,1) is also counted by
        #  _get_num_occupied_adjacent_seats, which then needs to be discounted.
        return EMPTY_SEAT
    else:
        return seat


@njit
def _get_visible_seat_matrix(row, column, all_seats):
    visible_seats = np.full((3, 3), FLOOR)
    if all_seats[row, column] == FLOOR:
        return visible_seats
    for i, j in np.ndindex(visible_seats.shape):
        if i == j == 1:
            continue
        cntr = 1
        row_diff = i - 1
        column_diff = j - 1
        # print(row_diff, column_diff)
        while (
            -1 < row + cntr * row_diff < all_seats.shape[0]
            and -1 < column + cntr * column_diff < all_seats.shape[1]
        ):
            seat_status = all_seats[row + cntr * row_diff, column + cntr * column_diff]
            # print(row + cntr * row_diff, column + cntr * column_diff, seat_status)
            if seat_status != FLOOR:
                visible_seats[i, j] = seat_status
                break
            cntr += 1
    # print(visible_seats)
    return visible_seats


@timer
def puzzle1_solution(seat_arrangement):
    # https://adventofcode.com/2020/day/11
    # This is kind of Conway's game of life
    print(seat_arrangement)

    for k in range(1000):
        temp = seat_arrangement.copy()
        # print(f'{k+1}e pass')
        for i, j in np.ndindex(temp.shape):
            seat_arrangement[i, j] = _get_seat_changes(
                temp[i, j],
                temp[max(0, i-1):i+2, max(0, j-1):j+2]
            )
        # print(seat_arrangement)
        if np.array_equal(seat_arrangement, temp):
            print(f'Equilibrium reached after {k} passes. Final seat plan:')
            print(seat_arrangement)
            break
    return _get_num_occupied_adjacent_seats(seat_arrangement)


@timer
def puzzle2_solution(seat_arrangement):
    # https://adventofcode.com/2020/day/11#part2
    print(seat_arrangement)
    for k in range(1000):
        temp = seat_arrangement.copy()
        # print(f'{k+1}e pass')
        for i, j in np.ndindex(temp.shape):
            # print(i, j, temp[i, j])
            seat_arrangement[i, j] = _get_seat_changes(
                temp[i, j],
                _get_visible_seat_matrix(i, j, temp)
            )
        # print(seat_arrangement)
        if np.array_equal(seat_arrangement, temp):
            print(f'Equilibrium reached after {k} passes. Final seat plan:')
            print(seat_arrangement)
            break
    return _get_num_occupied_adjacent_seats(seat_arrangement)


if __name__ == "__main__":
    main()
