from board import Board
from exceptions import GoalNotFoundError
from prototype.graph_search.graph_search_algorithm import GraphSearchAlgorithm
import custom_queue
import time
from algorithm import ResultType


class BFS(GraphSearchAlgorithm):
    def __init__(self, goal_test=Board.is_solved, las_vegas_randomization=False):
        super().__init__(goal_test)
        self.las_vegas_randomization = las_vegas_randomization

        self.path = None
        self.n_expanded = None

    def reset(self):
        self.path = None
        self.n_expanded = None

    def run(self, init_node):
        self.reset()
        open_nodes = custom_queue.FastLookupQueue()
        open_nodes.push_right(init_node)
        closed_nodes = set()

        start_time = time.time()

        while len(open_nodes) > 0:
            node = open_nodes.pop_left()
            if self.goal_test(node.board):
                self.path = node.path()

                self.results[ResultType.SOLUTION_COST] = len(self.path) - 1
                self.results[ResultType.EXPANDED_NODES] = len(closed_nodes) + 1
                self.results[ResultType.RUN_TIME] = time.time() - start_time

                return
            for child in node.children(shuffle=self.las_vegas_randomization):
                if (child not in open_nodes) and (child not in closed_nodes):
                    open_nodes.push_right(child)
            closed_nodes.add(node)

        raise GoalNotFoundError()
