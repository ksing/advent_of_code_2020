import itertools as it
import re
import sys
from pathlib import Path
from time import perf_counter

MASK_REG = re.compile(r'mask = ([X01]{36})')
MEMORY_REG = re.compile(r'mem\[(\d+)\] = (\d+)')


def main(file_name):
    t0 = perf_counter()
    print(f'Puzzle 1 solution: {puzzle1_solution(file_name)}')
    print(f'Time taken by puzzle1 = {perf_counter() - t0}')
    t0 = perf_counter()
    print(f'Puzzle 2 solution: {puzzle2_solution(file_name)}')
    print(f'Time taken by puzzle2 = {perf_counter() - t0}')


def puzzle1_solution(file_name):
    # https://adventofcode.com/2020/day/14
    memory_store = {}
    with open(file_name, 'r') as f:
        bitmask = MASK_REG.match(f.readline().strip()).group(1)
        for line in f:
            match = MEMORY_REG.match(line.strip())
            if match:
                memory_location, memory_value = match.groups()
                memory_store[int(memory_location)] = _get_bitmasked_value(int(memory_value), bitmask)
                continue
            match = MASK_REG.match(line.strip())
            if match:
                bitmask = match.group(1)
    return sum(memory_store.values())


def _get_bitmasked_value(memory, bitmask):
    new_memory = []
    for value, mask in zip(f'{memory:0>36b}', bitmask):
        if mask == 'X':
            new_memory.append(value)
        else:
            new_memory.append(mask)
    return int(''.join(new_memory), 2)


def puzzle2_solution(file_name):
    # https://adventofcode.com/2020/day/14#part2
    memory_store = {}
    with open(file_name, 'r') as f:
        bitmask = MASK_REG.match(f.readline().strip()).group(1)
        for line in f:
            match = MEMORY_REG.match(line.strip())
            if match:
                memory_location, memory_value = match.groups()
                for new_memory_location in _get_bitmasked_memory_address(int(memory_location), bitmask):
                    # print(new_memory_location)
                    memory_store[new_memory_location] = int(memory_value)
                continue
            match = MASK_REG.match(line.strip())
            if match:
                bitmask = match.group(1)
    # print(memory_store)
    return sum(memory_store.values())


def _get_bitmasked_memory_address(memory, bitmask):
    new_memory = []
    num_floating = 0
    for value, mask in zip(f'{memory:0>36b}', bitmask):
        if mask == 'X':
            new_memory.append(mask)
            num_floating += 1
        elif mask == '1':
            new_memory.append(mask)
        else:
            new_memory.append(value)
    for bit_replacements in it.product('01', repeat=num_floating):
        memory = ''.join(new_memory)
        for bit_replacement in bit_replacements:
            memory = memory.replace('X', bit_replacement, 1)
        yield int(memory, 2)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = Path(__file__).parent.resolve() / 'input.txt'
    main(file_name)
