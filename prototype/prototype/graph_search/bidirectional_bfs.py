from prototype.board import Board
from prototype.utils import FastLookupQueue
from prototype.algorithm import ResultType
import prototype.exceptions as exceptions
from prototype.graph_search.node import ForwardSearchNode, BackwardSearchNode
from prototype.graph_search.search_algorithms import GraphSearchAlgorithm
import time


class _GoalFoundSignal(Exception):
    pass


class BidirectionalBFS(GraphSearchAlgorithm):
    def __init__(self, las_vegas_randomization=False):
        super().__init__(goal_test=None)
        self.las_vegas_randomization = las_vegas_randomization

        self.path = None
        self.start_time = None
        self.open_nodes_forward = None
        self.open_nodes_backward = None
        self.closed_nodes_forward = None
        self.closed_nodes_backward = None
        self.init_board = None

    def _reset(self):
        self.path = None
        self.start_time = None
        self.open_nodes_forward = FastLookupQueue()
        self.open_nodes_backward = FastLookupQueue()
        self.closed_nodes_forward = set()
        self.closed_nodes_backward = set()

    def run(self, board):
        self._reset()
        self.init_board = board
        self.start_time = time.time()
        self.open_nodes_forward.push_right(ForwardSearchNode(board))
        goal_board = Board(board.N)
        self.open_nodes_backward.push_right(BackwardSearchNode(goal_board))

        try:
            while len(self.open_nodes_forward) > 0 and len(self.open_nodes_backward) > 0:
                self._forward_step()
                self._backward_step()
        except _GoalFoundSignal:
            return

        raise exceptions.GoalNotFoundError()

    def _forward_step(self):
        node = self.open_nodes_forward.pop_left()
        if node.board.is_solved():
            self._finalize(path=node.path())
            return
        elif node in self.open_nodes_backward:
            backward_node = self.open_nodes_backward.get(node)
            self._finalize(path=node.path() + backward_node.path()[1:])

        for child in node.children(shuffle=self.las_vegas_randomization):
            if (child not in self.open_nodes_forward) and (child not in self.closed_nodes_forward):
                self.open_nodes_forward.push_right(child)
        self.closed_nodes_forward.add(node)

    def _backward_step(self):
        node = self.open_nodes_backward.pop_left()
        if node.board == self.init_board:
            self._finalize(path=node.path())
            return
        elif node in self.open_nodes_forward:
            forward_node = self.open_nodes_forward.get(node)
            self._finalize(path=forward_node.path() + node.path()[1:])

        for child in node.children(shuffle=self.las_vegas_randomization):
            if (child not in self.open_nodes_backward) and (child not in self.closed_nodes_backward):
                self.open_nodes_backward.push_right(child)
        self.closed_nodes_backward.add(node)

    def _finalize(self, path):
        n_expanded = len(self.closed_nodes_forward) + len(self.closed_nodes_backward) + 1

        self.path = path
        self.results[ResultType.SOLUTION_COST.name] = len(self.path) - 1
        self.results[ResultType.EXPANDED_NODES.name] = n_expanded
        self.results[ResultType.RUN_TIME.name] = time.time() - self.start_time
        raise _GoalFoundSignal()

    def name(self):
        return "BiDirBFS"
