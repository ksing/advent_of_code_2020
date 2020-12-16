import operator as op
import re
import sys
from collections import defaultdict
from functools import reduce
from itertools import chain
from pathlib import Path
from time import perf_counter

DEFINITION_REG = re.compile(r'([a-z ]+): ([\d+-]+) (?:or ([\d+-]+))')


def main(file_name):
    with open(file_name, 'r') as f:
        definitions, my_ticket, other_tickets = f.read().split('\n\n')

    my_ticket = [int(number.strip()) for number in re.findall(r'(\d+)', my_ticket.strip())]
    other_tickets = [
        [int(number.strip()) for number in ticket.strip().split(',')]
        for ticket in other_tickets.split('\n')
        if re.match(r'\d+,', ticket)
    ]
    dict_definitions = _get_valid_definitions(definitions)

    t0 = perf_counter()
    print(f'Puzzle 1 solution: {puzzle1_solution(dict_definitions, other_tickets)}')
    print(f'Time taken by puzzle1 = {perf_counter() - t0}')
    t0 = perf_counter()
    print(f'Puzzle 2 solution: {puzzle2_solution(dict_definitions, my_ticket, other_tickets)}')
    print(f'Time taken by puzzle2 = {perf_counter() - t0}')


def puzzle1_solution(dict_definitions, other_tickets):
    # https://adventofcode.com/2020/day/16
    valid_numbers = set(chain.from_iterable(dict_definitions.values()))
    return sum(
        number for number in chain.from_iterable(other_tickets)
        if number not in valid_numbers
    )


def puzzle2_solution(dict_definitions, my_ticket, other_tickets):
    # https://adventofcode.com/2020/day/16#part2
    valid_numbers = set(chain.from_iterable(dict_definitions.values()))
    valid_tickets = [
        ticket for ticket in other_tickets
        if set(ticket) <= valid_numbers
    ]
    ticket_length = len(my_ticket)
    # If values at an index in all tickets satisfy the number range of a rule, add the index to the value
    #  in a dictionary with the name of the rule being the key.
    definition_indices = {}
    for definition, number_range in dict_definitions.items():
        definition_indices[definition] = {
            index
            for index in range(ticket_length)
            if all(ticket[index] in number_range for ticket in valid_tickets)
        }
    definition_indices = _get_definition_index_combinations(definition_indices)
    return reduce(op.mul, (
        my_ticket[set_index.pop()]
        for key, set_index in definition_indices.items()
        if key.startswith('departure')
    ))


def _get_valid_definitions(definitions):
    valid_definitions = defaultdict(set)
    for definition in definitions.split('\n'):
        key, *valid_ranges = DEFINITION_REG.match(definition.strip()).groups()
        for valid_range in valid_ranges:
            start, end = tuple(int(num) for num in valid_range.split('-'))
            valid_definitions[key] |= set(range(start, end + 1))
    return valid_definitions


def _get_definition_index_combinations(definition_indices):
    # Remove step-by-step indices from rule definitions, starting from that with least number of indices
    #  that satisfy its number range.
    seen = set()
    for definition, set_index in sorted(
        definition_indices.items(), key=lambda x: len(x[1])
    ):
        definition_indices[definition] = set_index - seen  # Remove indices already present in more specific rules.
        seen |= set_index

    # print(sorted(definition_indices.items(), key=lambda x: str(x[1])))
    # [('class', {0}), ('route', {1}), ('departure date', {2}), ('duration', {3}), ('arrival platform', {4}),
    #  ('arrival track', {5}), ('train', {6}), ('zone', {7}), ('row', {8}), ('departure location', {9}),
    #  ('departure station', {10}), ('arrival location', {11}), ('arrival station', {12}), ('price', {13}),
    #  ('wagon', {14}), ('seat', {15}), ('type', {16}), ('departure track', {17}),
    #  ('departure platform', {18}), ('departure time', {19})]
    return definition_indices


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = Path(__file__).parent.resolve() / 'input.txt'
    main(file_name)
