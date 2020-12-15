import sys
from pathlib import Path
from time import perf_counter


def main(file_name):
    t0 = perf_counter()
    print(f'Puzzle 1 solution: {puzzle1_solution(file_name)}')
    print(f'Time taken by puzzle1 = {perf_counter() - t0}')
    t0 = perf_counter()
    print(f'Puzzle 2 solution: {puzzle2_solution(file_name)}')
    print(f'Time taken by puzzle2 = {perf_counter() - t0}')


def read_file(file_name):
    with open(file_name, 'r') as f:
        for line in f:
            yield int(line.strip())


def puzzle1_solution(file_name):
    # https://adventofcode.com/2019/day/1
    return sum(module_weight // 3 - 2 for module_weight in read_file(file_name))


def puzzle2_solution(file_name):
    # https://adventofcode.com/2020/day/14#part2
    return sum(get_module_fuel(module_weight) for module_weight in read_file(file_name))


def get_module_fuel(mass):
    output = 0
    fuel_required = mass // 3 - 2
    if fuel_required <= 0:
        return 0
    return output + fuel_required + get_module_fuel(fuel_required)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = Path(__file__).parent.resolve() / 'input.txt'
    main(file_name)
