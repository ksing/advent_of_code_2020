from setuptools import setup
from Cython.Build import cythonize

setup(
    name='find_modulo_power', ext_modules=cythonize('find_modulo_power.pyx', )
)
