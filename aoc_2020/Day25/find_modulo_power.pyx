#cython: language_level=3
import cython


@cython.cfunc
cdef cython.ulong pow_mod(cython.ulong base, cython.ulong exponent, cython.ulong modulo):
    "Calculate (base ** exponent) % modulo efficiently."
    cdef cython.ulong number = 1
    while exponent:
        if exponent & 1:
            number = number * base % modulo
        exponent >>= 1
        base = base * base % modulo
    return number


cpdef cython.ulong modulo_power(cython.ulong card_public_key, cython.ulong door_public_key, cython.ulong subject_number):
    cdef cython.ulong divisor = 20201227
    cdef cython.ulong i
    for i in range(1, 10_000_000):
        if pow_mod(subject_number, i, divisor) == door_public_key:
            return pow_mod(card_public_key, i, divisor)
        if pow_mod(subject_number, i, divisor) == card_public_key:
            return pow_mod(door_public_key, i, divisor)
    else:
        return 0
