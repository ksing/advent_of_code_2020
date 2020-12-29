import sys
from collections import OrderedDict
from dataclasses import dataclass, field
from time import perf_counter
from typing import List, Optional


@dataclass
class Cup:
    value: int
    next: Optional['Cup'] = None
    smaller_cup: Optional['Cup'] = None

    def __repr__(self) -> str:
        next = None if self.next is None else self.next.value
        smaller_cup = None if self.smaller_cup is None else self.smaller_cup.value
        return f'{self.__class__.__name__}(value={self.value}, next={next}, smaller_cup={smaller_cup})'


@dataclass()
class CupsCircle:
    current_cup: Optional['Cup'] = field(init=False, default=None)
    largest_cup: Optional['Cup'] = field(init=False, default=None)
    head: Optional['Cup'] = None
    tail: Optional['Cup'] = None

    def __post_init__(self):
        if self.head is None and self.tail is not None:
            self.head = self.tail
            self.head.next = self.tail
            self.largest_cup = self.head
        elif self.head is not None and self.tail is None:
            self.tail = self.head
            self.head.next = self.tail
            self.largest_cup = self.head
        elif self.head is not None and self.tail is not None:
            self.head.next = self.tail
            self.tail.next = self.head
            if self.head.value > self.tail.value:
                self.largest_cup = self.head
            else:
                self.largest_cup = self.tail
        self.current_cup = self.head

    def add(self, cup: 'Cup'):
        if self.head is None:
            self.head = cup
            self.tail = cup
            self.largest_cup = cup
            self.current_cup = cup
            cup.next = cup
        else:
            self.tail.next = cup
            self.tail = cup
            self.tail.next = self.head
            if self.largest_cup.value < cup.value:
                self.largest_cup = cup

    def pop(self):
        if self.head is None:
            raise IndexError("Empty CircleQueue")
        else:
            deleted = self.head
            if self.largest_cup is self.head:
                self.largest_cup = self.head.smaller_cup
            self.head = self.head.next
            self.tail.next = self.head
            return deleted.value

    def remove(self):
        _ = self.pop()

    def insert(self, destination_cup, added_cups: List['Cup']):
        added_cups[-1].next = destination_cup.next
        destination_cup.next = added_cups[0]
        if destination_cup is self.tail:
            self.tail = added_cups[-1]

    def get_cup_label(self, value: int):
        cup = self.head
        while cup is not None:
            if cup.value == value:
                return cup
            cup = cup.next
            if cup is self.head:
                raise KeyError(f"No cup with the label {value}")

    def __str__(self) -> str:
        output = []
        cup = self.head
        while cup is not None:
            output.append(str(cup.value))
            if cup.next is self.head:
                break
            cup = cup.next
        return ''.join(output)


def main(cup_string):
    cups_dict = OrderedDict((int(cup), Cup(int(cup))) for cup in cup_string)
    t0 = perf_counter()
    print(f'Puzzle 1 solution: {puzzle1_solution(cups_dict)}')
    print(f'Time taken by puzzle1 = {perf_counter() - t0}')
    t0 = perf_counter()
    print(f'Puzzle 2 solution: {puzzle2_solution(cups_dict)}')
    print(f'Time taken by puzzle1 = {perf_counter() - t0}')


def _generate_cups_circle(cups_dict):
    cups_circle = CupsCircle()
    for cup_label, cup in cups_dict.items():
        cup.smaller_cup = cups_dict.get(cup_label - 1)
        cups_circle.add(cup)
    return cups_circle


def puzzle1_solution(cups_dict):
    # https://adventofcode.com/2020/day/23
    # print(cups_dict)
    cups_circle = _generate_cups_circle(cups_dict)
    print(cups_circle)
    cups_circle = perform_moves(cups_circle)
    cup_1 = cups_circle.get_cup_label(1)
    cup = cup_1.next
    output = []
    while cup != cup_1:
        output.append(str(cup.value))
        cup = cup.next
    return ''.join(output)


def puzzle2_solution(cups_dict):
    # https://adventofcode.com/2020/day/23#part2
    # print(cups_dict)
    cups_circle = _generate_cups_circle(cups_dict)
    print(cups_circle.__repr__())
    prev_cup = cups_circle.largest_cup
    for i in range(max(cups_dict.keys()) + 1, int(1e6 + 1)):
        cup = Cup(value=i, smaller_cup=prev_cup)
        cups_circle.add(cup)
        # print(cup, prev_cup)
        prev_cup = cup
    print(cups_circle.__repr__())
    cups_circle = perform_moves(cups_circle, num_moves=int(1e7))
    cup_1 = cups_circle.get_cup_label(1)
    cup_2 = cup_1.next
    cup_3 = cup_2.next
    print(cup_1, cup_2, cup_3)
    return cup_2.value * cup_3.value


def perform_moves(cups_circle, num_moves=100):
    for i in range(num_moves):
        # print(str(cups_circle), cups_circle.current_cup)
        picked_cups = [cups_circle.current_cup.next]
        for j in range(2):
            cup = picked_cups[j].next
            picked_cups.append(cup)
        # print('picked_cups:', picked_cups)
        cups_circle.current_cup.next = picked_cups[2].next
        destination_cup = cups_circle.current_cup.smaller_cup
        cups_circle.current_cup = cups_circle.current_cup.next
        while 1:
            # print('destination_cup:', destination_cup)
            if destination_cup is None:
                destination_cup = cups_circle.largest_cup
            if destination_cup not in picked_cups:
                break
            destination_cup = destination_cup.smaller_cup
        cups_circle.insert(destination_cup, picked_cups)
    return cups_circle


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cup_string = sys.argv[1]
    else:
        sys.exit('No input provide')
    main(cup_string)
