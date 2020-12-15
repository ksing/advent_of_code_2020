import itertools as it

import numpy as np


with open('./input.txt', 'r') as f:
    earliest_timestamp, bus_ids, *_ = [line.strip() for line in f]

valid_bus_ids = [int(bus_id) for bus_id in bus_ids.replace('x', '1').split(',')]
remainders = [-1 * index % num for index, num in enumerate(valid_bus_ids) if num > 1]
numbers = [num for num in valid_bus_ids if num > 1]
print(numbers)
print(remainders)

for a, b in it.combinations(numbers, 2):
    print(a, b, np.gcd(a, b))
