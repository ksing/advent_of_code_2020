import sys
from pathlib import Path
from time import perf_counter

import numpy as np

INACTIVE = '.'
ACTIVE = '#'


def main(file_name):
    with open(file_name, 'r') as f:
        input_data = [list(line.strip()) for line in f]
    t0 = perf_counter()
    print(f'Puzzle 1 solution: {puzzle1_solution(np.array(input_data))}')
    print(f'Time taken by puzzle1 = {perf_counter() - t0}')
    t0 = perf_counter()
    print(f'Puzzle 2 solution: {puzzle2_solution(np.array(input_data))}')
    print(f'Time taken by puzzle2 = {perf_counter() - t0}')


def puzzle1_solution(conway_cubes):
    # https://adventofcode.com/2020/day/17
    # Conway's game of cubes
    print(conway_cubes)
    conway_cubes = np.dstack(conway_cubes).T
    for m in range(6):
        conway_cubes = _expand_energy_source(conway_cubes)
        temp = conway_cubes.copy()
        print(f'{m+1}e pass.')
        for i, j, k in np.ndindex(temp.shape):
            # print(i, j, k)
            conway_cubes[i, j, k] = _change_cube_state(
                temp[i, j, k], temp[max(0, i-1):i+2, max(0, j-1):j+2, max(0, k-1):k+2]
            )
        # print(_get_num_activated_cubes(conway_cubes))
        # print('New energy config', conway_cubes)
    return _get_num_activated_cubes(conway_cubes)


def puzzle2_solution(conway_cubes):
    # https://adventofcode.com/2020/day/17#part2
    print(conway_cubes)
    conway_cubes = conway_cubes.reshape(conway_cubes.shape + (1, 1,))
    for m in range(6):
        conway_cubes = _expand_energy_source(conway_cubes, num_dimensions=4)
        temp = conway_cubes.copy()
        print(f'{m+1}e pass.')
        for i, j, k, l in np.ndindex(temp.shape):
            # print(i, j, k, l)
            conway_cubes[i, j, k, l] = _change_cube_state(
                temp[i, j, k, l], temp[max(0, i-1):i+2, max(0, j-1):j+2, max(0, k-1):k+2, max(0, l-1):l+2]
            )
        # print(_get_num_activated_cubes(conway_cubes))
        # print('New energy config', conway_cubes)
    return _get_num_activated_cubes(conway_cubes)


def _expand_energy_source(data, num_dimensions=3):
    new_shape = tuple(x + 2 for x in data.shape)
    out_matrix = np.full(new_shape, INACTIVE)
    if num_dimensions == 3:
        out_matrix[1:-1, 1:-1, 1:-1] = data
    elif num_dimensions == 4:
        out_matrix[1:-1, 1:-1, 1:-1, 1:-1] = data
    return out_matrix


def _change_cube_state(this_cube, adjacent_cubes):
    # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
    #  Otherwise, the cube becomes inactive.
    # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
    #  Otherwise, the cube remains inactive.
    if (
        (this_cube == INACTIVE and _get_num_activated_cubes(adjacent_cubes) == 3)
        or (this_cube == ACTIVE and _get_num_activated_cubes(adjacent_cubes) - 1 in (2, 3))
    ):
        return ACTIVE
    else:
        return INACTIVE


def _get_num_activated_cubes(energy_matrix):
    return (energy_matrix == ACTIVE).sum()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = Path(__file__).parent.resolve() / 'input.txt'
    main(file_name)
