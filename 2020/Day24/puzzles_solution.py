import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from time import perf_counter

import numpy as np
import scipy.ndimage


class TileColor(Enum):
    WHITE = 0
    BLACK = 1


@dataclass
class ArrayIndex:
    row: int
    column: int

    def __add__(self, other):
        return self.__class__(self.row + other.row, self.column + other.column)

    @property
    def as_tuple(self):
        return (self.row, self.column)


NEIGHBOURS = (
    ArrayIndex(0, 2),
    ArrayIndex(1, 1),
    ArrayIndex(1, -1),
    ArrayIndex(0, -2),
    ArrayIndex(-1, -1),
    ArrayIndex(-1, 1)
)
WIDTH = 200
HEIGHT = 200


def main(file_name):
    t0 = perf_counter()
    hexagonal_grid = _generate_hex_grid(HEIGHT, WIDTH)
    # num_tiles = hexagonal_grid.sum()
    # print(num_tiles)
    hexagonal_grid = puzzle1_solution(file_name, hexagonal_grid)
    print(f'Puzzle 1 solution: {(hexagonal_grid == TileColor.BLACK.value).sum()}')
    print(f'Time taken by puzzle1 = {perf_counter() - t0}')
    t0 = perf_counter()
    print(f'Puzzle 2 solution: {puzzle2_solution(hexagonal_grid)}')
    print(f'Time taken by puzzle2 = {perf_counter() - t0}')


def read_file(file_name):
    with open(file_name, 'r') as f:
        for line in f:
            yield line.strip()


def _generate_hex_grid(height, width=None):
    # Use the Even-only
    # http://roguebasin.roguelikedevelopment.org/index.php?title=Hexagonal_Tiles#Coordinate_systems_with_a_hex_grid
    if width is None:
        width = height
    return np.zeros((height, width), dtype=np.int8)


def puzzle1_solution(file_name, hexagonal_grid):
    # https://adventofcode.com/2020/day/24
    directions = 'e|se|sw|w|nw|ne'
    directions_reg = re.compile(f'({directions})')
    movements_dict = dict(zip(directions.split('|'), NEIGHBOURS))

    for line in read_file(file_name):
        index = ArrayIndex(row=HEIGHT // 2 - 1, column=WIDTH // 2 - 1)
        for instruction in directions_reg.findall(line):
            index += movements_dict[instruction]
        # print(index)
        hexagonal_grid[index.as_tuple] = 1 - hexagonal_grid[index.as_tuple]
        # print(hexagonal_grid[index.as_tuple])
    return hexagonal_grid


def puzzle2_solution(hexagonal_grid):
    # https://adventofcode.com/2020/day/24#part2
    weight_matrix = np.zeros((3, 5))
    for coords in NEIGHBOURS:
        weight_matrix[coords.row + 1, coords.column + 2] = 1

    for k in range(100):
        n_neighbours = scipy.ndimage.convolve(hexagonal_grid, weight_matrix)
        turn_white_mask = (hexagonal_grid == 1) & (np.logical_or(n_neighbours == 0, n_neighbours > 2))
        turn_black_mask = (hexagonal_grid == 0) & (n_neighbours == 2)
        # print(n_neighbours)
        hexagonal_grid[turn_black_mask] = 1
        hexagonal_grid[turn_white_mask] = 0
        num_black_tiles = (hexagonal_grid == TileColor.BLACK.value).sum()
        print(f'{num_black_tiles} black tiles after {k+1} days')
    return (hexagonal_grid == TileColor.BLACK.value).sum()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = Path(__file__).parent.resolve() / 'input.txt'  # type: ignore
    main(file_name)
