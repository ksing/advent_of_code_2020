from functools import reduce
from operator import mul


def chinese_remainder(modulos, remainders):
    output = 0
    product = reduce(mul, modulos)
    print(product)
    for modulo, remainder in zip(modulos, remainders):
        # print(modulo, remainder)
        p = product // modulo
        output += remainder * inverse_modulo_multiplier(p % modulo, modulo) * p
    return output % product


def inverse_modulo_multiplier(remainder, modulo, x=1, y=0):
    # remainder * x == 1 (mod modulo)
    m0 = modulo
    if modulo == 1:
        return 0
    while remainder > 1:
        # q is quotient
        y, x = x - (remainder // modulo) * y, y
        # m is remainder now, process same as Euclid's algo
        modulo, remainder = remainder % modulo, modulo
    # Make x positive
    if x < 0:
        x = x + m0
    return x


valid_bus_ids = [
    int(i) for i in
    '23,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,449,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,13,19,x,x,x,x,x,x,x,x,x,29,x,991,x,x,x,x,x,37,x,x,x,x,x,x,x,x,x,x,17'
    # '67,7,x,59,61'
    .replace('x', '1')
    .split(',')
]
remainders = [-1 * index % num for index, num in enumerate(valid_bus_ids) if num > 1]
numbers = [num for num in valid_bus_ids if num > 1]
print(numbers, remainders)
# for a, b in zip(remainders, numbers):
#     print(a, b, inverse_modulo_multiplier(a, b))
#     # print(gcd_extended(a, b))
print(int(chinese_remainder(numbers, remainders)))
