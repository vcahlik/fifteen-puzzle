from prototype.board import Board
from prototype.algorithm import Algorithm


class GraphSearchAlgorithm(Algorithm):
    def __init__(self, goal_test=Board.is_solved, metric=None):
        super().__init__(goal_test, metric)

    def run(self, init_node):
        pass
