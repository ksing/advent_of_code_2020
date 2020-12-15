from typing import Callable, ClassVar, Dict

from dataclasses import dataclass

import numpy as np


@dataclass
class Navigation:
    position_x: int = 0
    position_y: int = 0
    navigation_dict: ClassVar[Dict[str, Callable]] = {
        'N': lambda x: np.array([0, x]),
        'E': lambda x: np.array([x, 0]),
        'S': lambda x: np.array([0, -x]),
        'W': lambda x: np.array([-x, 0]),
    }

    def __post_init__(self):
        self.coordinates = np.array([self.position_x, self.position_y])

    def __repr__(self):
        return f'{self.__class__.__name__}({self.coordinates})'

    @staticmethod
    def rotation_matrix(theta):
        return np.array([
            [np.cos(theta), -1 * np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ]).round()

    def translate(self, move_direction, delta_position: int):
        self.coordinates += self.navigation_dict[move_direction](delta_position)

    def transform(self, turn_direction: str, turn_angle: int):
        if turn_direction == 'R':
            turn_angle *= -1
        rotation_matrix = self.rotation_matrix(turn_angle / 180 * np.pi)
        self.coordinates = np.dot(rotation_matrix, self.coordinates.reshape(2, 1)).reshape(2,).astype(int)

    def rotate(self, start_direction: str, turn_direction: str, turn_angle: int):
        if turn_direction == 'L':
            turn_angle *= -1
        direction_list = list(self.navigation_dict)
        return direction_list[
            (direction_list.index(start_direction) + turn_angle // 90) % len(direction_list)
        ]


class ShipNavigation(Navigation):

    def __init__(self, facing_direction: str, **kwargs):
        self.facing_direction = facing_direction
        super().__init__(**kwargs)

    def move(self, direction: str, delta_position: int):
        if direction == 'F':
            direction = self.facing_direction
        super().translate(direction, delta_position)

    def turn(self, turn_direction: str, times_turn: int):
        self.facing_direction = super().rotate(self.facing_direction, turn_direction, times_turn)

    @property
    def manhattan_distance(self):
        return np.abs(self.coordinates).sum()


class WayPoint(Navigation):

    def __init__(self, **kwargs):
        self.ship = ShipNavigation(facing_direction=None)
        super().__init__(**kwargs)

    def move_ship(self, forward_factor: int):
        self.ship.coordinates += self.coordinates * forward_factor

    def turn(self, turn_direction: str, turn_angle: int):
        super().transform(turn_direction, turn_angle)
