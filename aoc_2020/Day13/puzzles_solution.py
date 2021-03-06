import itertools as it
from functools import reduce
from operator import mul

from ..helper_functions import get_input_file_name, timer


def main():
    file_name = get_input_file_name(__file__)
    with open(file_name, 'r') as f:
        earliest_timestamp, bus_ids, *_ = [line.strip() for line in f]
    earliest_timestamp = int(earliest_timestamp)
    valid_bus_ids = [int(bus_id) for bus_id in bus_ids.replace('x', '0').split(',')]
    print(valid_bus_ids)
    print(f'Puzzle 1 solution: {puzzle1_solution(earliest_timestamp, valid_bus_ids)}')
    print(f'Puzzle 2 solution: {puzzle2_solution(valid_bus_ids)}')


@timer
def puzzle1_solution(earliest_timestamp, bus_ids):
    # https://adventofcode.com/2020/day/13
    for timestamp in it.count(earliest_timestamp):
        for bus_id in bus_ids:
            if bus_id and timestamp % bus_id == 0:
                return bus_id * (timestamp - earliest_timestamp)


@timer
def puzzle2_solution(bus_ids):
    # https://adventofcode.com/2020/day/13#part2
    remainders = [-1 * index % bus_id for index, bus_id in enumerate(bus_ids) if bus_id]
    valid_bus_ids = [bus_id for bus_id in bus_ids if bus_id]
    return chinese_remainder(valid_bus_ids, remainders)


def chinese_remainder(modulos, remainders):
    output = 0
    product = reduce(mul, modulos)
    # print(product)
    for modulo, remainder in zip(modulos, remainders):
        # print(modulo, remainder)
        p = product // modulo
        output += remainder * inverse_modulo_multiplier(p % modulo, modulo) * p
    return output % product


def inverse_modulo_multiplier(remainder, modulo):
    # remainder * x == 1 (mod modulo)
    m0 = modulo
    y = 0
    x = 1
    if modulo == 1:
        return 0
    while remainder > 1:
        # q is quotient
        y, x = x - (remainder // modulo) * y, y
        modulo, remainder = remainder % modulo, modulo
    # Don't go multiplying with negative numbers
    if x < 0:
        x = x + m0
    return x


if __name__ == "__main__":
    main()
