from prototype.graph_search.graph_search_algorithm import GraphSearchAlgorithm
from .dfs import DFS
from board import Board
from exceptions import GoalNotFoundError
import time
from algorithm import ResultType


class IDAStarSearch(GraphSearchAlgorithm):
    def __init__(self, heuristic=None, goal_test=Board.is_solved, las_vegas_randomization=False):
        super().__init__(goal_test)
        self.heuristic = heuristic
        self.las_vegas_randomization = las_vegas_randomization

    def reset(self):
        self.reset_results()

    def run(self, init_node):
        self.reset()
        initial_cost_limit = int(self.heuristic.estimate_cost(init_node.board))
        cost_limited_dfs = DFS(self.heuristic, self.goal_test, initial_cost_limit, self.las_vegas_randomization)
        n_expanded = 0

        start_time = time.time()

        while True:
            try:
                cost_limited_dfs.run(init_node)
                n_expanded = n_expanded + cost_limited_dfs.results[ResultType.EXPANDED_NODES.name]
            except GoalNotFoundError:
                cost_limited_dfs.cost_limit = cost_limited_dfs.cost_limit + 1
                n_expanded = n_expanded + cost_limited_dfs.results[ResultType.EXPANDED_NODES.name]
                continue

            self.results[ResultType.SOLUTION_COST.name] = cost_limited_dfs.cost_limit
            self.results[ResultType.EXPANDED_NODES.name] = n_expanded
            self.results[ResultType.RUN_TIME.name] = time.time() - start_time

            return
