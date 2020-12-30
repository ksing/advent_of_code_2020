import sys
from pathlib import Path
from time import perf_counter

DIVISOR = 20201227


def main(file_name):
    card_public_key, door_public_key = [
        int(key) for key in file_name.read_text().strip().splitlines()
    ]
    t0 = perf_counter()
    print(f"Puzzle 1 solution: {puzzle1_solution(card_public_key, door_public_key)}")
    print(f'Time taken by puzzle1 = {perf_counter() - t0}')
    # t0 = perf_counter()
    # print(f'Puzzle 2 solution: {puzzle2_solution(input_data)}')
    # print(f'Time taken by puzzle2 = {perf_counter() - t0}')


def puzzle1_solution(card_public_key, door_public_key):
    # https://adventofcode.com/2020/day/25
    subject_number = 7
    card_loop_size = None
    door_loop_size = None
    for i in range(10_000_000):
        if pow(subject_number, i, DIVISOR) == door_public_key:
            door_loop_size = i
        if pow(subject_number, i, DIVISOR) == card_public_key:
            card_loop_size = i
        if card_loop_size:
            return pow(door_public_key, card_loop_size, DIVISOR)
        if door_loop_size:
            return pow(card_public_key, door_loop_size, DIVISOR)
    else:
        print('Loop sizes not found')
        return None


def puzzle2_solution(input_data):
    # https://adventofcode.com/2020/day/25#part2
    return


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = Path(sys.argv[1]).resolve()
    else:
        file_name = Path(__file__).parent.resolve() / 'input.txt'  # type: ignore
    main(file_name)
