import re
from collections import deque
from copy import deepcopy

from ..helper_functions import get_input_file_name, timer


def main():
    file_name = get_input_file_name(__file__)
    with open(file_name, 'r') as f:
        dict_players = dict(
            parse_player_decks(player_data) for player_data in f.read().strip().split('\n\n')
        )
    print(f'Puzzle 1 solution: {puzzle1_solution(deepcopy(dict_players))}')
    #print(f'Puzzle 2 solution: {puzzle2_solution(deepcopy(dict_players))}')


def parse_player_decks(player_data):
    input_rows = player_data.splitlines()
    player_number = int(re.match(r'Player (\d+):', input_rows[0]).group(1))
    data = deque(int(row.strip()) for row in input_rows[1:])
    return player_number, data


@timer
def puzzle1_solution(dict_players):
    # https://adventofcode.com/2020/day/22
    winning_deck = _play_combat_game(dict_players)
    return _get_deck_score(winning_deck)


def _play_combat_game(dict_players):
    while dict_players[1] and dict_players[2]:
        card1, card2 = dict_players[1].popleft(), dict_players[2].popleft()
        if card1 > card2:
            dict_players[1] += [card1, card2]
        else:
            dict_players[2] += [card2, card1]
    print(dict_players)
    return dict_players[1] + dict_players[2]


@timer
def puzzle2_solution(dict_players):
    # https://adventofcode.com/2020/day/22#part2
    # print(dict_players)
    winner, dict_players = _play_recurse_combat_game(dict_players)
    print(dict_players)
    print(f"Winner: {winner}")
    return _get_deck_score(dict_players[winner])


def _play_recurse_combat_game(dict_players):
    deck_snapshots = [(dict_players[1].copy(), dict_players[2].copy())]
    winner = 0
    while dict_players[1] and dict_players[2]:
        # print(deck_snapshots)
        cards = dict_players[1].popleft(), dict_players[2].popleft()
        if cards[0] <= len(dict_players[1]) and cards[1] <= len(dict_players[2]):
            print('Starting a sub-game of Recursive combat')
            print(cards)
            print(dict_players.values())
            winner, _ = _play_recurse_combat_game(deepcopy(dict_players))
        else:
            winner = cards.index(max(cards)) + 1
        dict_players[winner] += [cards[(winner - 1) % 2], cards[winner % 2]]
        if (dict_players[1], dict_players[2]) in deck_snapshots:
            print('Configuration already exists')
            return 1, dict_players
        deck_snapshots.append((dict_players[1].copy(), dict_players[2].copy()))
    # print(dict_players)
    # print(f"Game {game_num} Winner: {winner}")
    return winner, dict_players


def _get_deck_score(deck):
    return sum((index + 1) * card_value for index, card_value in enumerate(reversed(deck)))


if __name__ == "__main__":
    main()
