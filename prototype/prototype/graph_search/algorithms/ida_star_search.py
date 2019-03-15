from prototype.graph_search.graph_search_algorithm import GraphSearchAlgorithm
from .dfs import DFS
from board import Board
from exceptions import GoalNotFoundError


class IDAStarSearch(GraphSearchAlgorithm):
    def __init__(self, heuristic, goal_test=Board.is_solved, metrics=None, las_vegas_randomization=False):
        super().__init__(goal_test, metrics)
        self.heuristic = heuristic
        self.las_vegas_randomization = las_vegas_randomization

    def run(self, init_node):
        # TODO fix the metric argument and expanded nodes count

        initial_cost_limit = self.heuristic.estimate_cost(init_node.board)
        cost_limited_dfs = DFS(self.heuristic, self.goal_test, initial_cost_limit, self.metric, self.las_vegas_randomization)

        while True:
            try:
                path, expanded_nodes = cost_limited_dfs.run(init_node)
                return path, expanded_nodes
            except GoalNotFoundError:
                cost_limited_dfs.cost_limit = cost_limited_dfs.cost_limit + 2
                continue
