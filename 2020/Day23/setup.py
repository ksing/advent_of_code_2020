from setuptools import setup
from Cython.Build import cythonize

setup(
    name='cups', ext_modules=cythonize('cups.pyx',), zip_safe=False
)
