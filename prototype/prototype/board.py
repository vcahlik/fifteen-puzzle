from enum import Enum
import array
import numpy as np
import hashlib
import random
import math


class Direction(Enum):
    """
    A direction in which the blank is moved.
    """
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def blank_pos_change(self, N):
        """
        Calculates the new position of the blank after it has been moved in the specified direction.
        """
        if self == Direction.UP:
            return N * -1
        elif self == Direction.DOWN:
            return N
        elif self == Direction.LEFT:
            return -1
        else:
            return 1

    def opposite(self):
        """
        Returns a direction opposite to the specified direction.
        """
        if self == Direction.UP:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.UP
        elif self == Direction.LEFT:
            return Direction.RIGHT
        else:
            return Direction.LEFT


class Board:
    """
    A (N^2-1)-puzzle board with pebbles.
    """
    _solved_config = {
        2: array.array('l', (1, 2, 3, 0)),
        3: array.array('l', (1, 2, 3, 4, 5, 6, 7, 8, 0)),
        4: array.array('l', (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)),
        5: array.array('l', (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 0))
    }

    _solved_blank_pos = {
        2: 3,
        3: 8,
        4: 15,
        5: 24
    }

    _IGNORED_PEBBLE = -1

    def __init__(self, N, config=None):
        """

        :param N: number of pebbles in a single row or column (NxN grid)
        :param config: the configuration of the pebbles
        """
        self.N = N
        if config is None:
            self.config = array.array('l', self._solved_config[self.N])
            self.blank_position = self._solved_blank_pos[self.N]
        else:
            assert N == math.sqrt(len(config))
            self.config = array.array('l', config)
            self.blank_position = self.pebble_positions()[0]

    def __str__(self):
        return str(np.array(self.config).reshape(self.N, self.N))

    def __eq__(self, other):
        return self.config == other.config

    def __hash__(self):
        return int(hashlib.sha1(self.config).hexdigest(), 16)

    def is_solved(self):
        """
        Determines whether the pebbles are in their goal configuration.
        """
        return self.config == self._solved_config[self.N]

    def position_to_index(self, position):
        """
        Returns a tuple with pos_x, pos_y
        """
        return position // self.N, position % self.N

    def valid_directions(self):
        """
        Gets directions in which the blank can be moved.

        :return: list of valid directions
        """
        directions = []
        row_index, col_index = self.position_to_index(self.blank_position)

        if row_index > 0:
            directions.append(Direction.UP)
        if row_index < self.N - 1:
            directions.append(Direction.DOWN)
        if col_index > 0:
            directions.append(Direction.LEFT)
        if col_index < self.N - 1:
            directions.append(Direction.RIGHT)

        return directions

    def pebble_positions(self):
        """
        Gets the list of positions of all pebbles.
        """
        positions = [None] * len(self.config)
        for position, pebble in enumerate(self.config):
            if pebble != self._IGNORED_PEBBLE:
                positions[pebble] = position
        return positions

    def pebble_positions_subset(self, pebbles):
        """
        Gets the list of positions of the specified pebbles.
        """
        pebble_positions = self.pebble_positions()
        subset = list()
        subset.append(pebble_positions[0])  # Empty pebble's position at beginning
        for pebble, position in enumerate(pebble_positions):
            if pebble in pebbles:
                subset.append(position)
        return subset

    def pebble_positions_subset_cpp(self, pebbles):
        """
        Specifically used by the C++ pattern database.
        """
        pebble_positions = self.pebble_positions()
        subset = list()
        subset.append(pebble_positions[0])  # Empty pebble's position at beginning

        for pebble in pebbles:
            if pebble in pebbles:
                subset.append(pebble_positions[pebble])
        return subset

    def pebble_indexes(self):
        """
        Gets the list of the indexes of all pebbles.
        """
        return [self.position_to_index(position) for position in self.pebble_positions()]

    def move_blank(self, direction):
        """
        Modifies the board by moving the blank to the specified direction.

        :return: the moved pebble
        """
        target_position = self.blank_position + direction.blank_pos_change(self.N)
        replaced_pebble = self.config[target_position]

        self.config[self.blank_position] = replaced_pebble
        self.config[target_position] = 0

        self.blank_position = target_position
        return replaced_pebble

    def _count_pebble_inversions(self):
        """
        Counts the number of inversions in the pebble positions. Used in the solvability check.

        Source: https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
        """
        n_inverses = 0
        for i in range(0, len(self.config)):
            for j in range(i + 1, len(self.config)):
                if (i != self.blank_position) \
                        and (j != self.blank_position) \
                        and (self.config[i] > self.config[j]):
                    n_inverses = n_inverses + 1
        return n_inverses

    def is_solvable(self):
        """
        Determines whether the board is solvable.

        Source: https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
        """
        n_inverses = self._count_pebble_inversions()
        blank_pos_y_from_bottom = self.N - 1 - self.position_to_index(self.blank_position)[0]

        N_is_odd = self.N % 2
        n_inverses_is_odd = n_inverses % 2
        blank_pos_y_from_bottom_is_odd = (blank_pos_y_from_bottom) % 2

        if N_is_odd:
            return bool(not n_inverses_is_odd)
        else:
            if blank_pos_y_from_bottom_is_odd:
                return bool(n_inverses_is_odd)
            else:
                return bool(not n_inverses_is_odd)

    def randomize(self, enforce_solvability=True):
        """
        Randomizes the positions of pebbles using a random permutation.
        """
        np.random.shuffle(self.config)
        self.blank_position = self.pebble_positions()[0]
        if enforce_solvability:
            while not self.is_solvable():
                np.random.shuffle(self.config)
                self.blank_position = self.pebble_positions()[0]
        return self

    def shuffle(self, n_moves_min=10000, randomize_n_moves: bool = True):
        """
        Randomly shuffles the pebbles.

        :param randomize_n_moves: randomly adds 1 to the n_moves, in order not to always end up with even or odd solution cost
        """
        last_direction = None

        n_moves = n_moves_min
        if randomize_n_moves:
            n_moves = n_moves + random.randint(0, 1)

        for _ in range(n_moves):
            directions = self.valid_directions()
            direction = random.choice(directions)
            if last_direction is not None and last_direction == direction.opposite():
                directions.remove(direction)
                direction = random.choice(directions)

            self.move_blank(direction)
            last_direction = direction

        return self

    # TODO rename
    def get_pebble_indexes(self, pebbles):
        return np.array([np.argwhere(self.config == i)[0] for i in pebbles])

    def to_partial(self, pebbles):
        """
        Converts the board to a partial board.
        """
        # TODO some issue here (invalid constructor arguments)
        return PartialBoard(self.get_pebble_indexes(pebbles), self.blank_position)


class PartialBoard(Board):
    """
    A partial board where some pebbles are ignored (don't have assigned numbers).

    Used in the calculation of the PDB heuristic.
    """

    def __init__(self, N, pebbles):
        """

        :param N: number of pebbles in a single row or column (NxN grid)
        :param pebbles: the pebbles which are not ignored
        """
        super().__init__(N=N)

        for i, pebble in enumerate(self.config):
            if pebble != 0 and pebble not in pebbles:
                self.config[i] = self._IGNORED_PEBBLE


class BoardsGenerator:
    """
    Base class for random boards generators.
    """

    def __init__(self, N):
        self.N = N

    def name(self):
        return self.__class__.__name__


class RandomBoardsGenerator(BoardsGenerator):
    """
    Generator of boards randomized by random permutations.
    """

    def __init__(self, N):
        super().__init__(N)

    def random_board(self):
        """
        Returns a randomized board.
        """
        board = Board(N=self.N)
        return board.randomize()

    def name(self):
        return "RND"


class ShufflingBoardsGenerator(BoardsGenerator):
    """
    Generator of boards randomized by random shuffling.
    """

    def __init__(self, N, n_shuffles, randomize_n_moves=True):
        super().__init__(N)
        self.n_shuffles = n_shuffles
        self.randomize_n_moves = randomize_n_moves

    def random_board(self):
        """
        Returns a shuffled board.
        """
        board = Board(N=self.N)
        return board.shuffle(self.n_shuffles, self.randomize_n_moves)

    def name(self):
        return f"SHF[Cnt:{self.n_shuffles}]"


class ChaoticShufflingBoardsGenerator(BoardsGenerator):
    """
    Generator of boards randomized by random shuffling, where the number of shuffles is random.
    """

    def __init__(self, N, n_shuffles_max):
        """

        :param N: number of pebbles in a single row or column (NxN grid)
        :param n_shuffles_max: maximum number of shuffles
        """
        super().__init__(N)
        self.n_shuffles_max = n_shuffles_max

    def random_board(self):
        """
        Returns a shuffled board.
        """
        board = Board(N=self.N)
        n_shuffles = random.randint(0, self.n_shuffles_max)
        return board.shuffle(n_shuffles, False)

    def name(self):
        return f"ChaoticSHF[MaxCnt:{self.n_shuffles_max}]"
