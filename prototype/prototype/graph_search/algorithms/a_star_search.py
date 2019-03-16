from prototype.graph_search.graph_search_algorithm import GraphSearchAlgorithm
import time
from custom_queue import PriorityQueue
from board import Board
from exceptions import GoalNotFoundError
from algorithm import ResultType


class AStarSearch(GraphSearchAlgorithm):
    def __init__(self, heuristic, goal_test=Board.is_solved, las_vegas_randomization=False):
        super().__init__(goal_test)
        self.heuristic = heuristic
        self.las_vegas_randomization = las_vegas_randomization

        self.path = None

    def reset(self):
        self.path = None
        self.reset_results()

    def run(self, init_node):
        self.reset()
        open_nodes = PriorityQueue()
        open_nodes.push(init_node, self.heuristic.estimate_cost(init_node.board))
        closed_nodes = set()

        start_time = time.time()

        while len(open_nodes) > 0:
            node = open_nodes.pop()
            if self.goal_test(node.board):
                self.path = node.path()

                self.results[ResultType.SOLUTION_COST] = len(self.path) - 1
                self.results[ResultType.EXPANDED_NODES] = len(closed_nodes) + 1
                self.results[ResultType.RUN_TIME] = time.time() - start_time

                return
            for child in node.children(shuffle=self.las_vegas_randomization):
                if child in closed_nodes:
                    continue
                curr_estimated_cost = open_nodes.get_priority(child)
                child_estimated_cost = child.estimate_cost + self.heuristic.estimate_cost(child.board)
                if curr_estimated_cost is None or curr_estimated_cost > child_estimated_cost:
                    open_nodes.push(child, child_estimated_cost)
                    closed_nodes.add(node)

        raise GoalNotFoundError()
