import sys
from array import array
from copy import copy
from time import perf_counter


def main(cup_string):
    cups_array = array('I', [int(cup) for cup in cup_string])
    t0 = perf_counter()
    print(f'Puzzle 1 solution: {puzzle1_solution(copy(cups_array))}')
    print(f'Time taken by puzzle1 = {perf_counter() - t0}')
    t0 = perf_counter()
    print(f'Puzzle 2 solution: {puzzle2_solution(copy(cups_array))}')
    print(f'Time taken by puzzle1 = {perf_counter() - t0}')


def _rearrange_array(input_array, label):
    start_index = input_array.index(label)
    return input_array[start_index:start_index+1] + input_array[start_index + 1:] + input_array[:start_index]


def puzzle1_solution(cups_array):
    # https://adventofcode.com/2020/day/23
    # print(cups_array)
    cups_array = perform_moves(cups_array)
    # print(cups_array)
    return ''.join([str(i) for i in _rearrange_array(cups_array, 1)])


def puzzle2_solution(cups_array):
    # https://adventofcode.com/2020/day/23#part2
    print(cups_array)
    print(max(cups_array), len(cups_array))
    cups_array.fromlist(list(range(max(cups_array) + 1, 1_000_001)))
    print(max(cups_array), len(cups_array))
    cups_array = perform_moves(cups_array, num_moves=int(1e7))
    index_of_1 = cups_array.index(1)
    print(index_of_1, cups_array[index_of_1:index_of_1 + 3])
    return cups_array[index_of_1 + 1] * cups_array[index_of_1 + 2]


def perform_moves(cups_array, num_moves=100):
    current_cup_label = cups_array[0]
    for i in range(num_moves):
        picked_cups = cups_array[1:4]
        destination_cup_label = current_cup_label - 1
        current_cup_label = cups_array[4]
        minimum_cup_label = min(cups_array[4:])
        while 1:
            if destination_cup_label in cups_array[4:]:
                break
            if destination_cup_label < minimum_cup_label:
                destination_cup_label = max(cups_array[4:])
                break
            destination_cup_label -= 1
        index = cups_array.index(destination_cup_label)
        cups_array = cups_array[:1] + cups_array[4:(index + 1)] + picked_cups + cups_array[(index + 1):]
        cups_array = _rearrange_array(cups_array, current_cup_label)
        if i % 10_000 == 0:
            print("That's 10k moves")
        # print(current_cup_label)
        # print(cups_array)
    return cups_array


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cup_string = sys.argv[1]
    else:
        sys.exit('No input provide')
    main(cup_string)
