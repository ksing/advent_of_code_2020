import sys
from collections import OrderedDict

from .cups import Cup, CupsCircle, extend_cups_circle, perform_moves
from ..helper_functions import timer


def main(cup_string):
    cups_dict = OrderedDict((int(cup), Cup(int(cup))) for cup in cup_string)
    print(f'Puzzle 1 solution: {puzzle1_solution(cups_dict)}')
    print(f'Puzzle 2 solution: {puzzle2_solution(cups_dict)}')


def _generate_cups_circle(cups_dict):
    cups_circle = CupsCircle(None, None)
    for cup_label, cup in cups_dict.items():
        cup.smaller_cup = cups_dict.get(cup_label - 1)
        cups_circle.add(cup)
    return cups_circle


@timer
def puzzle1_solution(cups_dict):
    # https://adventofcode.com/2020/day/23
    # print(cups_dict)
    cups_circle = _generate_cups_circle(cups_dict)
    print(cups_circle)
    cups_circle = perform_moves(cups_circle)
    cup_1 = cups_circle.get_cup_label(1)
    cup = cup_1.next
    output = []
    while cup != cup_1:
        output.append(str(cup.value))
        cup = cup.next
    return ''.join(output)


@timer
def puzzle2_solution(cups_dict):
    # https://adventofcode.com/2020/day/23#part2
    # print(cups_dict)
    cups_circle = _generate_cups_circle(cups_dict)
    prev_cup = cups_circle.largest_cup
    cups_circle = extend_cups_circle(cups_circle, prev_cup, max(cups_dict.keys()), int(1e6))
    cups_circle = perform_moves(cups_circle, num_moves=int(1e7))
    cup_1 = cups_circle.get_cup_label(1)
    cup_2 = cup_1.next
    cup_3 = cup_2.next
    print(cup_1, cup_2, cup_3)
    return cup_2.value * cup_3.value


if __name__ == "__main__":
    if len(sys.argv[1]) > 2:
        cup_string = sys.argv[1]
    else:
        sys.exit('No input provided')
    main(cup_string)
