import re
import sys
from collections import deque
from pathlib import Path
from time import perf_counter

EXPRESSION_REG = re.compile(r'\([^\(\)]+\)')
PARANTHESIS_REG = re.compile(r'[\(\)]')
ADDITION_REG = re.compile(r'\b\d+ \+ \d+\b')


def main(file_name):
    t0 = perf_counter()
    print(f'Puzzle 1 solution: {puzzle1_solution(file_name)}')
    print(f'Time taken by puzzle1 = {perf_counter() - t0}')
    t0 = perf_counter()
    print(f'Puzzle 2 solution: {puzzle2_solution(file_name)}')
    print(f'Time taken by puzzle2 = {perf_counter() - t0}')


def get_expression_result(line, evaluation_func):
    # print(line, end=' -> ')
    while PARANTHESIS_REG.search(line):
        for expr in EXPRESSION_REG.findall(line):
            line = line.replace(expr, str(evaluation_func(expr)), 1)
    # print(line, end=': ')
    output = evaluation_func(line)
    # print(output)
    return output


def _evaluate_expression_left_to_right(expr):
    expr = PARANTHESIS_REG.sub('', expr).strip().split()
    if len(expr) == 1:
        return eval(expr[0])
    new_expr = ' '.join([str(eval(' '.join(expr[:3])))] + expr[3:])
    return _evaluate_expression_left_to_right(new_expr)


def puzzle1_solution(file_name):
    # https://adventofcode.com/2020/day/17
    # Conway's game of cubes
    return sum(
        get_expression_result(line, _evaluate_expression_left_to_right)
        for line in read_file(file_name)
    )


def _evaluate_expression_add_first(expr):
    while ' + ' in expr:
        for addition in ADDITION_REG.findall(expr):
            expr = expr.replace(addition, str(eval(addition)), 1)
    return _evaluate_expression_left_to_right(expr)


def puzzle2_solution(file_name):
    # https://adventofcode.com/2020/day/18#part2
    return sum(
        get_expression_result(line, _evaluate_expression_add_first) for line in read_file(file_name)
    )


def read_file(file_name):
    with open(file_name, 'r') as f:
        for line in f:
            yield line.strip()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = Path(__file__).parent.resolve() / 'input.txt'
    main(file_name)
