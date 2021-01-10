import itertools as it
import operator as op
import re
from collections import namedtuple
from dataclasses import dataclass
from functools import reduce
from pathlib import Path

import numpy as np

from ..helper_functions import get_input_file_name, timer

TileSides = namedtuple('TileSides', ['left', 'top', 'right', 'bottom'])


@dataclass
class Tile:
    tile_name: int
    tile_data: np.array
    num_tile_matches: int = 0

    def __post_init__(self):
        self.matching_tiles = {0: None, 1: None, 2: None, 3: None}

    @property
    def sides(self):
        return TileSides(
            left=self.tile_data[:, 0],
            top=self.tile_data[0, :],
            right=self.tile_data[:, -1],
            bottom=self.tile_data[-1, :]
        )

    @classmethod
    def parse_input(cls, input_data):
        input_rows = input_data.replace('.', '0').replace('#', '1').splitlines()
        tile_name = int(re.match(r'Tile (\d+):', input_rows[0]).group(1))
        data = np.array([
            list(row.strip()) for row in input_rows[1:]
        ], dtype=np.int8)
        return tile_name, cls(tile_name, data)

    def rotate(self):
        self.tile_data = np.rot90(self.tile_data, k=3)
        self.matching_tiles.update({
            0: self.matching_tiles[3],
            1: self.matching_tiles[0],
            2: self.matching_tiles[1],
            3: self.matching_tiles[2]
        })

    def flip_left_right(self):
        self.tile_data = np.fliplr(self.tile_data)
        self.matching_tiles.update({
            0: self.matching_tiles[2],
            2: self.matching_tiles[0]
        })

    def flip_upside_down(self):
        self.tile_data = np.flipud(self.tile_data)
        self.matching_tiles.update({
            1: self.matching_tiles[3],
            3: self.matching_tiles[1]
        })

    def __repr__(self):
        return f'{self.__class__.__name__}({self.tile_name})'

    def __str__(self):
        return f'Tile {self.tile_name}:\n{str(self.tile_data)}'

    def trim(self):
        self.tile_data = self.tile_data[1:-1, 1:-1]


def main():
    file_name = get_input_file_name(__file__)
    with open(file_name, 'r') as f:
        input_data = f.read().strip().split('\n\n')

    image_tiles = match_image_tiles(
        dict(Tile.parse_input(tile_input) for tile_input in input_data)
    )
    print(f'Puzzle 1 solution: {puzzle1_solution(image_tiles)}')
    print(f'Puzzle 2 solution: {puzzle2_solution(image_tiles)}')


@timer
def match_image_tiles(image_tiles):
    # https://adventofcode.com/2020/day/20
    side_list = TileSides._fields
    for tile1, tile2 in it.combinations(image_tiles.values(), 2):
        flag = 0
        for side_1, side_1_data in zip(side_list, tile1.sides):
            for side_2, side_2_data in zip(side_list, tile2.sides):
                if (
                    np.array_equal(side_1_data, side_2_data)
                    or np.array_equal(side_1_data, np.flip(side_2_data))
                ):
                    flag = 1
                    tile1.matching_tiles[side_list.index(side_1)] = tile2.tile_name
                    tile2.matching_tiles[side_list.index(side_2)] = tile1.tile_name
                    break
            if flag:
                tile1.num_tile_matches += 1
                tile2.num_tile_matches += 1
                break
    return image_tiles


@timer
def puzzle1_solution(image_tiles):
    corner_tiles = (tile.tile_name for tile in image_tiles.values() if tile.num_tile_matches == 2)
    return reduce(op.mul, corner_tiles)


@timer
def puzzle2_solution(image_tiles):
    # https://adventofcode.com/2020/day/20#part2
    image = _get_joined_image(image_tiles)
    # print(image.shape)
    monster_image = _read_monster_image()
    # print(monster_image)
    return image.sum() - _get_turbulence_under_monster(image, monster_image)


def _get_turbulence_under_monster(image, monster_image):
    num_turbulence_under_monster = 0
    list_operations = (np.fliplr, np.flipud, lambda x: x)
    for i in range(len(image)):
        for j in range(len(image)):
            flag = 0
            for k in range(4):
                for func in list_operations:
                    test_monster_image = func(np.rot90(monster_image, k=k))
                    matching_image = image[i:i + test_monster_image.shape[0], j:j + test_monster_image.shape[1]]
                    if test_monster_image.shape == matching_image.shape:
                        if np.array_equiv(np.logical_and(test_monster_image, matching_image), test_monster_image):
                            # print(test_monster_image)
                            # print(matching_image)
                            # print('match', i, i + test_monster_image.shape[0], j, j + test_monster_image.shape[1])
                            flag = 1
                            num_turbulence_under_monster += test_monster_image.sum()
                            break
                if flag:
                    break
    return num_turbulence_under_monster


def _get_joined_image(image_tiles):
    index_change_dict = {
        0: (0, -1),
        1: (-1, 0),
        2: (0, 1),
        3: (1, 0)
    }
    image_array_size = np.sqrt(len(image_tiles)).astype(int)

    def _create_image_array(image_array, tile, index):
        image_array[index] = tile.tile_name
        # print(tile.tile_name, tile.matching_tiles)
        if np.alltrue(image_array):
            return image_array
        # print(image_array)
        for side, tile_name in sorted(tile.matching_tiles.items()):
            if tile_name and tile_name not in image_array:
                break
        while 1:
            matching_side = [
                key for key, value in image_tiles[tile_name].matching_tiles.items()
                if value == tile.tile_name
            ][0]
            if side == matching_side:
                if side in (0, 2):
                    image_tiles[tile_name].flip_left_right()
                else:
                    image_tiles[tile_name].flip_upside_down()
            elif (side + matching_side) % 2 == 1:
                image_tiles[tile_name].rotate()
            else:
                if np.array_equiv(tile.sides[side], image_tiles[tile_name].sides[matching_side]):
                    del image_tiles[tile_name].matching_tiles[matching_side]
                    # print(removed_tile)
                    index = tuple(x + delta for delta, x in zip(index_change_dict[side], index))
                    break
                elif np.array_equiv(tile.sides[side], np.flip(image_tiles[tile_name].sides[matching_side])):
                    if side in (1, 3):
                        image_tiles[tile_name].flip_left_right()
                    else:
                        image_tiles[tile_name].flip_upside_down()
        return _create_image_array(image_array, image_tiles[tile_name], index)

    for tile_name, tile in image_tiles.items():
        if tile.num_tile_matches == 2 and tile.matching_tiles.get(0) and tile.matching_tiles.get(3):
            print(tile_name, tile.matching_tiles)
            break
    size_tiles = len(tile.tile_data) - 2
    image_array = _create_image_array(
        np.zeros((image_array_size, image_array_size), dtype=np.int32),
        tile,
        (0, image_array_size - 1)
    )
    print(image_array)
    image_data = np.zeros((image_array_size * size_tiles, image_array_size * size_tiles), dtype=np.int8)
    for i in range(image_array_size):
        for j in range(image_array_size):
            image_tiles[image_array[i, j]].trim()
            image_data[
                i * size_tiles:(i + 1) * size_tiles,
                j * size_tiles:(j + 1) * size_tiles
            ] = image_tiles[image_array[i, j]].tile_data
    return image_data


def _read_monster_image():
    with open(Path(__file__).parent.resolve() / 'sea_monster.txt') as f:
        return np.array([
            list(line.replace(' ', 'X').replace('X', '0').replace('#', '1').strip())
            for line in f
        ], dtype=np.int8)


if __name__ == "__main__":
    main()
