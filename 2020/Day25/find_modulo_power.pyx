#cython: language_level=3


cdef unsigned long pow_mod(unsigned long base, unsigned long exponent, unsigned long modulo):
    "Calculate (base ** exponent) % modulo efficiently."
    cdef unsigned long number = 1
    while exponent:
        if exponent & 1:
            number = number * base % modulo
        exponent >>= 1
        base = base * base % modulo
    return number


cpdef unsigned long modulo_power(unsigned long card_public_key, unsigned long door_public_key, unsigned long subject_number):
    cdef unsigned long divisor = 20201227
    cdef unsigned long i
    for i in range(10_000_000):
        if pow_mod(subject_number, i, divisor) == door_public_key:
            return pow_mod(card_public_key, i, divisor)
        if pow_mod(subject_number, i, divisor) == card_public_key:
            return pow_mod(door_public_key, i, divisor)
    else:
        return 0
