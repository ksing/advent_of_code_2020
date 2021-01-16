import re

from ..helper_functions import get_input_file_name, timer
from .classes import ShipNavigation, WayPoint

NAVIGATION_REG = re.compile(r'([NSEWLRF])(\d+)')


def main():
    file_name = get_input_file_name(__file__)
    with open(file_name, 'r') as f:
        input_data = [line.strip() for line in f]
    print(f'Puzzle 1 solution: {puzzle1_solution(input_data)}')
    print(f'Puzzle 2 solution: {puzzle2_solution(input_data)}')


@timer
def puzzle1_solution(navigation_instructions):
    # https://adventofcode.com/2020/day/12
    ship = ShipNavigation(facing_direction='E')
    # print(ship)
    for instruction in navigation_instructions:
        # print(instruction)
        navigation, value = NAVIGATION_REG.match(instruction).groups()
        if navigation in ('L', 'R'):
            ship.turn(navigation, int(value))
        else:
            ship.move(navigation, int(value))
        # print(ship)
    return ship.manhattan_distance


@timer
def puzzle2_solution(navigation_instructions):
    # https://adventofcode.com/2020/day/12#part2
    relative_way_point = WayPoint(position_x=10, position_y=1)
    for instruction in navigation_instructions:
        # print(instruction)
        navigation, value = NAVIGATION_REG.match(instruction).groups()
        if navigation in ('L', 'R'):
            relative_way_point.turn(navigation, int(value))
        elif navigation == 'F':
            relative_way_point.move_ship(int(value))
        else:
            relative_way_point.translate(navigation, int(value))
        # print(relative_way_point)
        # print(relative_way_point.ship)
    return relative_way_point.ship.manhattan_distance


if __name__ == "__main__":
    main()
