import re
from typing import NamedTuple

from ..helper_functions import get_input_file_name, timer


class AccInstruction(NamedTuple):
    acc_value: int = 0
    jmp_value: int = 0

    def __add__(self, other):
        return self.__class__(
            self.acc_value + other.acc_value,
            self.jmp_value + other.jmp_value
        )


INSTRUCTION_REGEX = re.compile(r'(?P<instruction>acc|nop|jmp) (?P<value>[+-]\d+)$')


def main():
    file_name = get_input_file_name(__file__)
    with open(file_name, 'r') as f:
        input_data = [line.strip() for line in f]
    print(f'Puzzle 1 solution: {puzzle1_solution(input_data)}')
    print(f'Puzzle 2 solution: {puzzle2_solution(input_data)}')


@timer
def puzzle1_solution(input_data):
    acc_code_line = AccInstruction()
    seen = set()
    while acc_code_line.jmp_value < len(input_data):
        seen.add(acc_code_line.jmp_value)
        # print(acc_code_line)
        acc_code_line += _parse_instruction(input_data[acc_code_line.jmp_value])
        if acc_code_line.jmp_value in seen:
            print(f'Infinte loop has begun with {acc_code_line}')
            break
    else:
        print('Program terminated correctly.')
    return acc_code_line.acc_value


@timer
def puzzle2_solution(input_data):
    acc_code_line = AccInstruction()
    seen = set()
    line_numbers_changed = []
    is_changed = False
    while acc_code_line.jmp_value < len(input_data):
        seen.add(acc_code_line.jmp_value)
        # print(acc_code_line)
        instruction_output = _parse_instruction(input_data[acc_code_line.jmp_value])
        if (
            instruction_output.jmp_value != 1
            and not is_changed
            and acc_code_line.jmp_value not in line_numbers_changed
        ):
            line_numbers_changed.append(acc_code_line.jmp_value)
            # print(f'Changing line number {acc_code_line.jmp_value}')
            instruction_output = AccInstruction(0, 1)
            is_changed = True
        acc_code_line += instruction_output
        if acc_code_line.jmp_value in seen:
            # print(f'Infinte loop has begun with {acc_code_line}')
            seen.clear()
            acc_code_line = AccInstruction()
            is_changed = False
    else:
        print(f'Program terminated correctly by changing line #{ line_numbers_changed[-1] + 1}.')
    return acc_code_line.acc_value


def _parse_instruction(instruction):
    try:
        instruction, value = INSTRUCTION_REGEX.match(instruction).groups()
    except AttributeError:
        raise
    if instruction == 'acc':
        return AccInstruction(int(value), 1)
    elif instruction == 'jmp':
        return AccInstruction(0, int(value))
    else:
        return AccInstruction(0, 1)


if __name__ == "__main__":
    main()
