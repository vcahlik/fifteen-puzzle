from board import Board
from .heuristic import Heuristic


class ManhattanDistanceHeuristic(Heuristic):
    def __init__(self, custom_name=None):
        super().__init__(custom_name)
        self._solved_indexes = Board().pebble_indexes()[1:]

    def estimate_cost(self, board):
        indexes = board.pebble_indexes()[1:]
        pebble_costs = [abs(index[0] - solved_index[0]) + abs(index[1] - solved_index[1])
                        for index, solved_index in zip(indexes, self._solved_indexes)]
        return sum(pebble_costs)
