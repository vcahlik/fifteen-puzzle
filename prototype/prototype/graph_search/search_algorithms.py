from prototype.board import Board
from prototype.algorithm import Algorithm
from prototype.utils import FastLookupQueue, PriorityQueue
from prototype.algorithm import ResultType
import prototype.exceptions as exceptions
from prototype.graph_search.node import ForwardSearchNode
import time


class GraphSearchAlgorithm(Algorithm):
    def __init__(self, goal_test=Board.is_solved):
        super().__init__(goal_test)

    def run(self, board):
        pass


class BFS(GraphSearchAlgorithm):
    def __init__(self, goal_test=Board.is_solved, las_vegas_randomization=False):
        super().__init__(goal_test)
        self.las_vegas_randomization = las_vegas_randomization

        self.path = None

    def _reset(self):
        self.path = None

    def run(self, board):
        self._reset()
        open_nodes = FastLookupQueue()
        open_nodes.push_right(ForwardSearchNode(board))
        closed_nodes = set()

        start_time = time.time()

        while len(open_nodes) > 0:
            node = open_nodes.pop_left()
            if self.goal_test(node.board):
                self.path = node.path()

                self.results[ResultType.SOLUTION_COST.name] = len(self.path) - 1
                self.results[ResultType.EXPANDED_NODES.name] = len(closed_nodes) + 1
                self.results[ResultType.RUN_TIME.name] = time.time() - start_time

                return
            for child in node.children(shuffle=self.las_vegas_randomization):
                if (child not in open_nodes) and (child not in closed_nodes):
                    open_nodes.push_right(child)
            closed_nodes.add(node)

        raise exceptions.GoalNotFoundError()

    def name(self):
        return "BFS"


class DFS(GraphSearchAlgorithm):
    def __init__(self, heuristic=None, goal_test=Board.is_solved, cost_limit=None, las_vegas_randomization=False):
        super().__init__(goal_test)
        self.heuristic = heuristic
        self.cost_limit = cost_limit
        self.las_vegas_randomization = las_vegas_randomization

        self.path = None

    def reset(self):
        self.path = None

    def run(self, board):
        self.reset()
        open_nodes = FastLookupQueue()
        open_nodes.push_right(ForwardSearchNode(board))
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
        raise exceptions.GoalNotFoundError()

    def name(self):
        return f"DFS"


class AStarSearch(GraphSearchAlgorithm):
    def __init__(self, heuristic=None, goal_test=Board.is_solved, las_vegas_randomization=False):
        super().__init__(goal_test)
        self.heuristic = heuristic
        self.las_vegas_randomization = las_vegas_randomization

        self.path = None

    def reset(self):
        self.path = None
        self.reset_results()

    def run(self, board):
        self.reset()
        open_nodes = PriorityQueue()
        open_nodes.push(ForwardSearchNode(board), self.heuristic.estimate_cost(board))
        closed_nodes = set()

        self.results[ResultType.INITIAL_HEURISTIC_PREDICTION.name] = self.heuristic.estimate_cost(board)
        start_time = time.time()

        while len(open_nodes) > 0:
            node = open_nodes.pop()
            if self.goal_test(node.board):
                self.path = node.path()

                self.results[ResultType.SOLUTION_COST.name] = len(self.path) - 1
                self.results[ResultType.EXPANDED_NODES.name] = len(closed_nodes) + 1
                self.results[ResultType.RUN_TIME.name] = time.time() - start_time

                return
            for child in node.children(shuffle=self.las_vegas_randomization):
                if child in closed_nodes:
                    continue
                curr_estimated_cost = open_nodes.get_priority(child)
                child_estimated_cost = child.cost + self.heuristic.estimate_cost(child.board)
                if curr_estimated_cost is None or curr_estimated_cost > child_estimated_cost:
                    open_nodes.push(child, child_estimated_cost)
                    closed_nodes.add(node)

        raise exceptions.GoalNotFoundError()

    def name(self):
        return "A*"


class IDAStarSearch(GraphSearchAlgorithm):
    def __init__(self, heuristic=None, goal_test=Board.is_solved, las_vegas_randomization=False):
        super().__init__(goal_test)
        self.heuristic = heuristic
        self.las_vegas_randomization = las_vegas_randomization

        self.path = None

    def reset(self):
        self.path = None
        self.reset_results()

    def run(self, board):
        self.reset()
        initial_cost_limit = int(self.heuristic.estimate_cost(board))
        cost_limited_dfs = DFS(self.heuristic, self.goal_test, initial_cost_limit, self.las_vegas_randomization)
        n_expanded = 0

        self.results[ResultType.INITIAL_HEURISTIC_PREDICTION.name] = self.heuristic.estimate_cost(board)
        start_time = time.time()

        while True:
            try:
                cost_limited_dfs.run(board)
                n_expanded = n_expanded + cost_limited_dfs.results[ResultType.EXPANDED_NODES.name]
            except exceptions.GoalNotFoundError:
                cost_limited_dfs.cost_limit = cost_limited_dfs.cost_limit + 1
                n_expanded = n_expanded + cost_limited_dfs.results[ResultType.EXPANDED_NODES.name]
                continue

            self.path = cost_limited_dfs.path

            self.results[ResultType.SOLUTION_COST.name] = cost_limited_dfs.cost_limit
            self.results[ResultType.EXPANDED_NODES.name] = n_expanded
            self.results[ResultType.RUN_TIME.name] = time.time() - start_time

            return

    def name(self):
        return "IDA*"
