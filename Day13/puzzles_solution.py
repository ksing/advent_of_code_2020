import itertools as it
import sys
from pathlib import Path
from time import perf_counter


def main(file_name):
    with open(file_name, 'r') as f:
        earliest_timestamp, bus_ids, *_ = [line.strip() for line in f]
    earliest_timestamp = int(earliest_timestamp)
    valid_bus_ids = [int(bus_id) for bus_id in bus_ids.replace('x', '1').split(',')]
    print(valid_bus_ids)
    t0 = perf_counter()
    print(f'Puzzle 1 solution: {puzzle1_solution(earliest_timestamp, valid_bus_ids)}')
    print(f'Time taken by puzzle1 = {perf_counter() - t0}')
    t0 = perf_counter()
    print(f'Puzzle 2 solution: {puzzle2_solution(valid_bus_ids)}')
    print(f'Time taken by puzzle2 = {perf_counter() - t0}')


def puzzle1_solution(earliest_timestamp, bus_ids):
    # https://adventofcode.com/2020/day/13
    for timestamp in it.count(earliest_timestamp):
        for bus_id in bus_ids:
            if bus_id > 1 and timestamp % bus_id == 0:
                return bus_id * (timestamp - earliest_timestamp)


def puzzle2_solution(bus_ids):
    # https://adventofcode.com/2020/day/13#part2
    max_bus_id = max(bus_ids)
    index_max_id = bus_ids.index(max_bus_id)
    for timestamp in it.count(max_bus_id, step=max_bus_id):
        # print(timestamp)
        if all(
            bus_id and (timestamp + index - index_max_id) % bus_id == 0
            for index, bus_id in enumerate(bus_ids)
        ):
            return timestamp


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = Path(__file__).parent.resolve() / 'input.txt'
    main(file_name)
