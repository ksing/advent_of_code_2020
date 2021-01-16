from .find_modulo_power import modulo_power
from ..helper_functions import get_input_file_name, timer


def main():
    file_name = get_input_file_name(__file__)
    card_public_key, door_public_key = [
        int(key) for key in file_name.read_text().strip().splitlines()
    ]
    print(f"Puzzle 1 solution: {puzzle1_solution(card_public_key, door_public_key)}")


@timer
def puzzle1_solution(card_public_key, door_public_key):
    # https://adventofcode.com/2020/day/25
    subject_number = 7
    return modulo_power(card_public_key, door_public_key, subject_number)


if __name__ == "__main__":
    main()
