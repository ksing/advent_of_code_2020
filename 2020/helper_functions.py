import sys
from functools import wraps
from pathlib import Path
from time import perf_counter


def timer(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = perf_counter()
        result = func(*args, **kwargs)
        print(f'Time taken by {func.__name__} = {perf_counter() - t0}')
        return result

    return wrapper


def get_input_file_name(file_):
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return Path(file_).parent.resolve() / 'input.txt'
