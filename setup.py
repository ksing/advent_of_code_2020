from setuptools import Extension, setup
from Cython.Build import cythonize

setup(name='advent_of_code', zip_safe=False, ext_modules=cythonize([
    Extension('*', ['2020/Day25/find_modulo_power.pyx']),
    Extension('*', ['2020/Day23/cups.pyx']),
]))
