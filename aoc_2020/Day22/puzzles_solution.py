import re
from collections import deque
from copy import deepcopy
from itertools import islice

from ..helper_functions import get_input_file_name, timer


def main():
    file_name = get_input_file_name(__file__)
    with open(file_name, 'r') as f:
        dict_players = dict(
            parse_player_decks(player_data) for player_data in f.read().strip().split('\n\n')
        )
    print(f'Puzzle 1 solution: {puzzle1_solution(deepcopy(dict_players))}')
    print(f'Puzzle 2 solution: {puzzle2_solution(deepcopy(dict_players))}')


def parse_player_decks(player_data):
    input_rows = player_data.splitlines()
    player_number = int(re.match(r'Player (\d+):', input_rows[0]).group(1)) - 1
    data = deque(int(row.strip()) for row in input_rows[1:])
    return player_number, data


@timer
def puzzle1_solution(dict_players):
    # https://adventofcode.com/2020/day/22
    winning_deck = _play_combat_game(dict_players)
    return _get_deck_score(winning_deck)


def _play_combat_game(dict_players):
    while dict_players[0] and dict_players[1]:
        cards = dict_players[0].popleft(), dict_players[1].popleft()
        winner = cards.index(max(cards))
        dict_players[winner].extend([cards[winner % 2], cards[(winner + 1) % 2]])
    print(dict_players)
    return dict_players[0] + dict_players[1]


@timer
def puzzle2_solution(dict_players):
    # https://adventofcode.com/2020/day/22#part2
    # print(dict_players)
    winner, dict_players = _play_recursive_combat_game(dict_players)
    print(dict_players)
    print(f"Winner: {winner}")
    return _get_deck_score(dict_players[winner])


def _create_cards_snapshot(player_1_deck, player_2_deck):
    return (
        ' '.join([str(card) for card in player_1_deck])
        + '\t'
        + ' '.join([str(card) for card in player_2_deck])
    )


def _play_recursive_combat_game(dict_players):
    deck_snapshots = set()
    winner = -1
    while dict_players[0] and dict_players[1]:
        snapshot = _create_cards_snapshot(dict_players[0], dict_players[1])
        if snapshot in deck_snapshots:
            # print('Configuration already exists')
            return 0, dict_players
        else:
            deck_snapshots.add(snapshot)
        cards = dict_players[0].popleft(), dict_players[1].popleft()
        if cards[0] <= len(dict_players[0]) and cards[1] <= len(dict_players[1]):
            subgame_dict_players = {
                i: deque(islice(dict_players[i], 0, cards[i]))
                for i in (0, 1)
            }
            winner, _ = _play_recursive_combat_game(subgame_dict_players)
        else:
            winner = cards.index(max(cards))
        dict_players[winner].extend([cards[winner % 2], cards[(winner + 1) % 2]])
    return winner, dict_players


def _get_deck_score(deck):
    return sum((index + 1) * card_value for index, card_value in enumerate(reversed(deck)))


if __name__ == "__main__":
    main()
