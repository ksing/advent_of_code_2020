import sys
from collections import OrderedDict
from dataclasses import dataclass, field
from time import perf_counter
from typing import Optional


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
            deleted = self.head.value
            if self.largest_cup is self.head:
                self.largest_cup = self.head.smaller_cup
            self.tail.next = self.head.next
            del self.head
            return deleted

    def remove(self):
        _ = self.pop()

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
            output.append(cup.value)
            if cup is self.tail:
                break
            cup = cup.next
        return ''.join(output)


def main(cup_string):
    cups_dict = OrderedDict((int(cup), Cup(int(cup))) for cup in cup_string)
    t0 = perf_counter()
    print(f'Puzzle 1 solution: {puzzle1_solution(cups_dict)}')
    print(f'Time taken by puzzle1 = {perf_counter() - t0}')
    # t0 = perf_counter()
    # print(f'Puzzle 2 solution: {puzzle2_solution(cups_dict)}')
    # print(f'Time taken by puzzle1 = {perf_counter() - t0}')


def _generate_cups_circle(cups_dict):
    cups_circle = CupsCircle()
    for cup_label, cup in cups_dict.items():
        cup.smaller_cup = cups_dict.get(cup_label - 1)
        cups_circle.add(cup)
    return cups_circle


def puzzle1_solution(cups_dict):
    # https://adventofcode.com/2020/day/23
    print(cups_dict)
    cups_circle = _generate_cups_circle(cups_dict)
    print(cups_circle)
    cups_circle = perform_moves(cups_circle)
    print(cups_circle)
    print(cups_circle.get_cup_label(1))
    # return ''.join([str(i) for i in _rearrange_array(cups_dict, 1)])


# def puzzle2_solution(cups_dict):
#     # https://adventofcode.com/2020/day/23#part2
#     print(cups_dict)
#     print(max(cups_dict), len(cups_dict))
#     cups_dict.fromlist(list(range(max(cups_dict) + 1, 1_000_001)))
#     print(max(cups_dict), len(cups_dict))
#     cups_dict = perform_moves(cups_dict, num_moves=int(1e7))
#     index_of_1 = cups_dict.index(1)
#     print(index_of_1, cups_dict[index_of_1:index_of_1 + 3])
#     return cups_dict[index_of_1 + 1] * cups_dict[index_of_1 + 2]


def perform_moves(cups_circle, num_moves=100):
    for i in range(num_moves):
        print(str(cups_circle))
        picked_cups = [cups_circle.current_cup.next]
        for j in range(2):
            cup = picked_cups[j].next
            picked_cups.append(cup)
        print(picked_cups)
        cups_circle.current_cup.next = picked_cups[2].next
        destination_cup = cups_circle.current_cup.smaller_cup
        cups_circle.current_cup = cups_circle.current_cup.next
        while 1:
            if destination_cup is None:
                destination_cup = cups_circle.largest_cup
            if destination_cup not in picked_cups:
                break
            destination_cup = destination_cup.smaller_cup
        picked_cups[2].next = destination_cup.next
        destination_cup.next = picked_cups[0]
        if i % 10_000 == 0:
            print("That's 10k moves")
        # print(current_cup_label)
        # print(cups_dict)
    return cups_circle


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cup_string = sys.argv[1]
    else:
        sys.exit('No input provide')
    main(cup_string)
