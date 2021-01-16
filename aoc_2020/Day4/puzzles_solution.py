import re

from ..helper_functions import get_input_file_name, timer


def main():
    file_name = get_input_file_name(__file__)
    with open(file_name, 'r') as f:
        passports_list = [
            passport.strip().replace('\n', ' ') for passport in f.read().split('\n\n')
        ]
    print(f'Number of passports = {len(passports_list)}')
    print(f'Puzzle 1 solution: {puzzle1_solution(passports_list)}')
    print(f'Puzzle 2 solution: {puzzle2_solution(passports_list)}')


@timer
def puzzle1_solution(passports_list):
    dict_reg = {
        'Birth Year': re.compile(r'\bbyr:\S'),
        'Issue Year': re.compile(r'\biyr:\S'),
        'Expiration Year': re.compile(r'\beyr:\S'),
        'Height': re.compile(r'\bhgt:\S'),
        'Hair Color': re.compile(r'\bhcl:\S'),
        'Eye Color': re.compile(r'\becl:\S'),
        'Passport ID': re.compile(r'\bpid:\S'),
        # 'Country ID': re.compile(r'\bcid:\d+\b'),
    }
    return sum(
        all(reg.search(passport) for reg in dict_reg.values())
        for passport in passports_list
    )


@timer
def puzzle2_solution(passports_list):
    dict_reg = {
        'Birth Year': re.compile(r'\bbyr:(?:19[2-9][0-9]|200[0-2])\b'),
        'Issue Year': re.compile(r'\biyr:20(?:1[0-9]|20)\b'),
        'Expiration Year': re.compile(r'\beyr:20(?:2[0-9]|30)\b'),
        'Height': re.compile(r'\bhgt:(?:1(?:[5-8][0-9]|9[0-3])cm|(?:59|6[0-9]|7[0-6])in)\b'),
        'Hair Color': re.compile(r'\bhcl:\#[a-f0-9]{6}\b'),
        'Eye Color': re.compile(r'\becl:(?:amb|blu|brn|gry|grn|hzl|oth)\b'),
        'Passport ID': re.compile(r'\bpid:\d{9}\b'),
        # 'Country ID': re.compile(r'\bcid:\d+\b'),
    }
    return sum(
        all(reg.search(passport) for reg in dict_reg.values())
        for passport in passports_list
    )


if __name__ == "__main__":
    main()
