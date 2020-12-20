import re
import sys
from functools import lru_cache
from pathlib import Path
from time import perf_counter

RULE_REG = re.compile(r'(\d+): (.+)')


def main(file_name):
    with open(file_name, 'r') as f:
        rules, messages = f.read().split('\n\n')
    t0 = perf_counter()
    print(f'Puzzle 1 solution: {puzzle1_solution(rules, messages)}')
    print(f'Time taken by puzzle1 = {perf_counter() - t0}')


def puzzle1_solution(rules, messages):
    # https://adventofcode.com/2020/day/19
    rules_dict = dict(
        tuple(RULE_REG.match(rule.replace('"', '').strip()).groups())
        for rule in rules.strip().splitlines()
    )
    # print(rules_dict)
    rules_dict = _rules_to_regexes(dict(rules_dict))
    # print(rules_dict[0])
    # print(messages)
    return sum(
        re.match(rules_dict[0], message.strip()) is not None
        for message in messages.splitlines()
    )


def _rules_to_regexes(rules_dict):
    cntr = 0
    for key, value in rules_dict.items():
        # print(key, ': ', value)
        value = value.strip()
        if re.search(r'\d+', value):
            cntr += 1
            for rule_num in re.findall(r'\d+', value):
                string_value = rules_dict[rule_num].strip()
                # print(string_value)
                if re.search(r'\d+', string_value):
                    continue
                if '|' in string_value:
                    string_value = f'(?:{string_value})'
                value = re.sub(f'(?:^|\D){rule_num}(?:$|\D)', f' {string_value} ', value)
            rules_dict[key] = value
    if cntr == 0:
        return {int(key): value.replace(' ', '') + '$' for key, value in rules_dict.items()}
    else:
        return _rules_to_regexes(rules_dict)


def _rules_to_regexes2(rules_dict, key):
    cntr = 0
    value = rules_dict[key].strip()
    for rule_num in re.findall(r'\d+', value):
        string_value = _rules_to_regexes2(rules_dict, rule_num)
        print(rule_num, string_value)
        if re.search(r'\d+', string_value):
            cntr += 1
            if '|' in string_value:
                string_value = f'(?:{string_value})'
            value = re.sub(f'(?:^|\D){rule_num}(?:$|\D)', f' {string_value} ', value)
    rules_dict[key] = value
    if cntr == 0:
        return {int(key): value.replace(' ', '') + '$' for key, value in rules_dict.items()}
    else:
        return _rules_to_regexes2(rules_dict)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = Path(__file__).parent.resolve() / 'input.txt'
    main(file_name)
