from enum import Enum
import array
import copy
import numpy as np
import hashlib
import random


class Direction(Enum):
    up = -4
    down = 4
    left = -1
    right = 1

    def opposite(self):
        if self == Direction.up:
            return Direction.down
        elif self == Direction.down:
            return Direction.up
        elif self == Direction.left:
            return Direction.right
        else:
            return Direction.left


class Board:
    _solved_config = array.array('l', (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0))
    _solved_blank_pos = 15

    _IGNORED_PEBBLE = -1

    def __init__(self, config=None):
        if config is None:
            self.config = array.array('l', self._solved_config)
            self.blank_position = self._solved_blank_pos
        else:
            self.config = array.array('l', config)
            self.blank_position = self.pebble_positions()[0]

    def __str__(self):
        return str(np.array(self.config).reshape(4, 4))

    def __eq__(self, other):
        return self.config == other.config

    def __hash__(self):
        return int(hashlib.sha1(self.config).hexdigest(), 16)

    def is_solved(self):
        return self.config == self._solved_config

    @staticmethod
    def position_to_index(position):
        return position // 4, position % 4

    def valid_directions(self):
        directions = []
        row_index, col_index = self.position_to_index(self.blank_position)

        if row_index > 0:
            directions.append(Direction.up)
        if row_index < 3:
            directions.append(Direction.down)
        if col_index > 0:
            directions.append(Direction.left)
        if col_index < 3:
            directions.append(Direction.right)

        return directions

    def pebble_positions(self):
        positions = [None] * 16
        for position, pebble in enumerate(self.config):
            if pebble != self._IGNORED_PEBBLE:
                positions[pebble] = position
        return positions

    def pebble_positions_subset(self, pebbles):
        pebble_positions = self.pebble_positions()
        subset = list()
        subset.append(pebble_positions[0])  # Empty pebble's position at beginning
        for pebble, position in enumerate(pebble_positions):
            if pebble in pebbles:
                subset.append(position)
        return subset

    def pebble_indexes(self):
        return [self.position_to_index(position) for position in self.pebble_positions()]

    def move_blank(self, direction):
        target_position = self.blank_position + direction.value
        replaced_pebble = self.config[target_position]

        self.config[self.blank_position] = replaced_pebble
        self.config[target_position] = 0

        self.blank_position = target_position
        return replaced_pebble

    # def randomize(self):
    #     np.random.shuffle(self.config)
    #     while not self.is_solvable():
    #         np.random.shuffle(self.config)

    # def is_solvable(self):
    #     TODO check using permutation sign and distance of blank from goal
        # return True

    def shuffle(self, n_moves=1000):
        last_direction = None
        for _ in range(n_moves):
            directions = self.valid_directions()
            direction = random.choice(directions)
            if last_direction is not None and last_direction == direction.opposite():
                directions.remove(direction)
                direction = random.choice(directions)

            self.move_blank(direction)
            last_direction = direction

    def get_pebble_indexes(self, pebbles):
        return np.array([np.argwhere(self.config == i)[0] for i in pebbles])

    def to_partial(self, pebbles):
        return PartialBoard(self.get_pebble_indexes(pebbles), self.blank_position)


class PartialBoard(Board):
    def __init__(self, pebbles):
        super().__init__()

        for i, pebble in enumerate(self.config):
            if pebble != 0 and pebble not in pebbles:
                self.config[i] = self._IGNORED_PEBBLE
