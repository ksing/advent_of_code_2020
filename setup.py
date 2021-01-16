from setuptools import Extension, setup
from Cython.Build import cythonize

setup(name='advent_of_code', zip_safe=False, ext_modules=cythonize([
    Extension('*', ['aoc_2020/Day*/*.pyx']),
]))
