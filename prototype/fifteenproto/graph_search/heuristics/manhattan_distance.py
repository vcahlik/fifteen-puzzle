from board import Board


class ManhattanDistanceHeuristic:
    def __init__(self):
        self._solved_indexes = Board().pebble_indexes()[1:]

    def cost(self, board):
        indexes = board.pebble_indexes()[1:]
        pebble_costs = [abs(index[0] - solved_index[0]) + abs(index[1] - solved_index[1])
                        for index, solved_index in zip(indexes, self._solved_indexes)]
        return sum(pebble_costs)
