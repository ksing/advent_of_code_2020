from ..helper_functions import get_input_file_name, timer

DIVISOR = 20201227


def main():
    file_name = get_input_file_name(__file__)
    card_public_key, door_public_key = [
        int(key) for key in file_name.read_text().strip().splitlines()
    ]
    print(f"Puzzle 1 solution: {puzzle1_solution(card_public_key, door_public_key)}")
    # print(f'Puzzle 2 solution: {puzzle2_solution(input_data)}')


@timer
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


@timer
def puzzle2_solution(input_data):
    # https://adventofcode.com/2020/day/25#part2
    return


if __name__ == "__main__":
    main()
