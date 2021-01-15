from ..helper_functions import get_input_file_name, timer


def main():
    file_name = get_input_file_name(__file__)
    print(f'Puzzle 1 solution: {puzzle1_solution(file_name)}')
    print(f'Puzzle 2 solution: {puzzle2_solution(file_name)}')


def read_file(file_name):
    with open(file_name, 'r') as f:
        for line in f:
            yield int(line.strip())


@timer
def puzzle1_solution(file_name):
    # https://adventofcode.com/2019/day/1
    return sum(module_weight // 3 - 2 for module_weight in read_file(file_name))


@timer
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
    main()
