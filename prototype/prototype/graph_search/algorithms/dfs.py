from prototype.graph_search.graph_search_algorithm import GraphSearchAlgorithm
from prototype.custom_queue import FastLookupQueue
from board import Board
from exceptions import GoalNotFoundError


class DFS(GraphSearchAlgorithm):
    def __init__(self, heuristic, goal_test=Board.is_solved, cost_limit=None, metric=None, las_vegas_randomization=False):
        super().__init__(goal_test, metric)
        self.heuristic = heuristic
        self.cost_limit = cost_limit
        self.las_vegas_randomization = las_vegas_randomization

        self.path = None
        self.n_expanded = None

    def reset(self):
        self.path = None
        self.n_expanded = 0

    def run(self, init_node):
        self.reset()
        open_nodes = FastLookupQueue()
        open_nodes.push_right(init_node)

        while len(open_nodes) > 0:
            node = open_nodes.pop_right()
            self.n_expanded = self.n_expanded + 1
            if self.goal_test(node.board):
                self.path = node.path()
                return
            for child in node.children(shuffle=self.las_vegas_randomization):
                estimated_cost = child.cost + self.heuristic.estimate_cost(child.board)
                if estimated_cost <= self.cost_limit:
                    open_nodes.push_right(child)

        raise GoalNotFoundError()
