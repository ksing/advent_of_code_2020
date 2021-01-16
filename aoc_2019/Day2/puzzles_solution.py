import itertools as it
from array import array

from ..helper_functions import get_input_file_name, timer


def main():
    file_name = get_input_file_name(__file__)
    with open(file_name, 'r') as f:
        input_data = [int(num) for num in ''.join(f.readlines()).strip().split(',')]
    print(f"Puzzle 1 solution: {puzzle1_solution(array('q', input_data))}")
    print(f'Puzzle 2 solution: {puzzle2_solution(input_data)}')


@timer
def puzzle1_solution(input_array):
    # https://adventofcode.com/2019/day/2
    return _process_int_code(input_array)


@timer
def puzzle2_solution(input_data):
    # https://adventofcode.com/2020/day/14#part2
    noun, verb = 12, 2
    for noun, verb in it.product(range(100), repeat=2):
        data = array('q', input_data)
        data[1] = noun
        data[2] = verb
        if _process_int_code(data) == 19690720:
            return 100 * noun + verb


def _process_int_code(input_array):
    index = 0
    while index < len(input_array):
        if input_array[index] == 99:
            break
        elif input_array[index] == 1:
            position1, position2, output_position = input_array[index + 1:index + 4]
            input_array[output_position] = input_array[position1] + input_array[position2]
        elif input_array[index] == 2:
            position1, position2, output_position = input_array[index + 1:index + 4]
            input_array[output_position] = input_array[position1] * input_array[position2]
        else:
            print(f'Something has gone wrong! Unexpected opcode. {input_array[index]}')
        index += 4
    # print(input_array)
    return input_array[0]


if __name__ == "__main__":
    main()
