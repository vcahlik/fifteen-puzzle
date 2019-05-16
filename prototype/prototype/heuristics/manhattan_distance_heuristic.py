from prototype.board import Board
from prototype.heuristics.heuristic import Heuristic


class ManhattanDistanceHeuristic(Heuristic):
    def __init__(self, N):
        self._solved_indexes = Board(N=N).pebble_indexes()[1:]

    def estimate_cost(self, board):
        indexes = board.pebble_indexes()[1:]
        pebble_costs = [abs(index[0] - solved_index[0]) + abs(index[1] - solved_index[1])
                        for index, solved_index in zip(indexes, self._solved_indexes)]
        return sum(pebble_costs)

    def name(self):
        return "MD"
