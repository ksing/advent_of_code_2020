import re
import sys
from collections import defaultdict

RULE_REG = re.compile(
    r'(?P<container>(?:\w+ ){1,2})bags? contains?(?P<contained_bags>( \d+(?: \w+){1,2} bags?[,\.])+)'
)
BAG_REG = re.compile(r'(?P<number>\d+)(?P<color>(?: \w+){1,2}) bag')


def main(file_name):
    with open(file_name, 'r') as f:
        inner_bag_dict, outer_bag_dict = _get_bag_rules(
            [line.replace(' no ', ' 0 ').strip() for line in f]
        )
    print(f'Puzzle 1 solution: {puzzle1_solution(inner_bag_dict, "shiny gold")}')
    print(f'Puzzle 2 solution: {puzzle2_solution(outer_bag_dict, "shiny gold")}')


def puzzle1_solution(bag_contain_dict, bag_color):

    def _get_num_outermost_bag_colors(color):
        list_color_bags = []
        if color in bag_contain_dict:
            for key in bag_contain_dict[color]:
                # print(key)
                list_color_bags.append(key)
                list_color_bags += _get_num_outermost_bag_colors(key)
        return list_color_bags

    set_color_bags = set(_get_num_outermost_bag_colors(bag_color))
    return len(set_color_bags)


def puzzle2_solution(bag_contain_dict, bag_color):

    def _get_num_inner_bags(color):
        num_bags = 0
        if color in bag_contain_dict:
            for color_bag, num_bag in bag_contain_dict[color].items():
                # print(color_bag, num_bag)
                num_bags += num_bag + (_get_num_inner_bags(color_bag) * num_bag)
                # print(num_bags)
        return num_bags

    return _get_num_inner_bags(bag_color)


def _get_bag_rules(rules_list):
    outer_bag_dict = defaultdict(dict)
    inner_bag_dict = defaultdict(dict)
    for rule in rules_list:
        match = RULE_REG.match(rule)
        if match:
            # print(match.groupdict())
            outer_bag = match['container'].strip()
            for bag in BAG_REG.finditer(match['contained_bags']):
                num_bags = int(bag['number'])
                inner_bag = bag['color'].strip()
                if num_bags:
                    # print(bag.groups())
                    inner_bag_dict[inner_bag].update({outer_bag: num_bags})
                    outer_bag_dict[outer_bag].update({inner_bag: num_bags})
    # print(bag_contain_dict)
    return inner_bag_dict, outer_bag_dict


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = './input.txt'
    main(file_name)
