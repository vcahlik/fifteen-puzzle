from prototype.graph_search.graph_search_algorithm import GraphSearchAlgorithm
from prototype.custom_queue import FastLookupQueue
from board import Board
from exceptions import GoalNotFoundError
import time
from algorithm import ResultType


class DFS(GraphSearchAlgorithm):
    def __init__(self, heuristic=None, goal_test=Board.is_solved, cost_limit=None, las_vegas_randomization=False):
        super().__init__(goal_test)
        self.heuristic = heuristic
        self.cost_limit = cost_limit
        self.las_vegas_randomization = las_vegas_randomization

        self.path = None

    def reset(self):
        self.path = None

    def run(self, init_node):
        self.reset()
        open_nodes = FastLookupQueue()
        open_nodes.push_right(init_node)
        n_expanded = 0

        start_time = time.time()

        while len(open_nodes) > 0:
            node = open_nodes.pop_right()
            n_expanded = n_expanded + 1
            if self.goal_test(node.board):
                self.path = node.path()

                self.results[ResultType.SOLUTION_COST.name] = len(self.path) - 1
                self.results[ResultType.EXPANDED_NODES.name] = n_expanded
                self.results[ResultType.RUN_TIME.name] = time.time() - start_time

                return
            for child in node.children(shuffle=self.las_vegas_randomization):
                estimated_cost = child.cost + self.heuristic.estimate_cost(child.board)
                if estimated_cost <= self.cost_limit:
                    open_nodes.push_right(child)

        self.results[ResultType.EXPANDED_NODES.name] = n_expanded
        self.results[ResultType.RUN_TIME.name] = time.time() - start_time
        raise GoalNotFoundError()
