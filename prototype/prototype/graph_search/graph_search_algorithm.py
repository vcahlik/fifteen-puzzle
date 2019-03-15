from prototype.board import Board
from prototype.algorithm import Algorithm


class GraphSearchAlgorithm(Algorithm):
    def __init__(self, goal_test=Board.is_solved, metrics: list = None):
        super().__init__(goal_test, metrics)

    def run(self, init_node):
        pass
