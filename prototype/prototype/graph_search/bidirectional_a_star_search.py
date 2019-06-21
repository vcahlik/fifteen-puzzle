from prototype.board import Board
from prototype.utils import PriorityQueue
from prototype.algorithm import ResultType
from prototype.exceptions import GoalNotFoundError
from prototype.graph_search.node import ForwardSearchNode, BackwardSearchNode
from prototype.graph_search.search_algorithms import GraphSearchAlgorithm
import time


class _GoalFoundSignal(Exception):
    pass


class BidirectionalAStarSearch(GraphSearchAlgorithm):
    def __init__(self, forward_heuristic=None, backward_heuristic=None, las_vegas_randomization=False):
        super().__init__(goal_test=None)
        self.forward_heuristic = forward_heuristic
        self.backward_heuristic = backward_heuristic
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
        self.open_nodes_forward = PriorityQueue()
        self.open_nodes_backward = PriorityQueue()
        self.closed_nodes_forward = set()
        self.closed_nodes_backward = set()

    def run(self, board):
        self._reset()
        self.init_board = board
        self.backward_heuristic.set_goal(board)
        self.open_nodes_forward.push(ForwardSearchNode(board), self.forward_heuristic.estimate_cost(board))
        goal_board = Board(board.N)
        self.open_nodes_backward.push(BackwardSearchNode(goal_board), self.backward_heuristic.estimate_cost(goal_board))

        self.results[ResultType.INITIAL_HEURISTIC_PREDICTION.name] = self.forward_heuristic.estimate_cost(board)
        self.start_time = time.time()

        try:
            while len(self.open_nodes_forward) > 0 and len(self.open_nodes_backward) > 0:
                self._forward_step()
                self._backward_step()
        except _GoalFoundSignal:
            return

        raise GoalNotFoundError()

    def _forward_step(self):
        node = self.open_nodes_forward.pop()
        if node.board.is_solved():
            self._finalize(path=node.path())
        elif node in self.closed_nodes_backward:
            # TODO
            backward_node = self.closed_nodes_backward.get(node)
            self._finalize(path=node.path().concatenate(backward_node.path()))

        for child in node.children(shuffle=self.las_vegas_randomization):
            if child in self.closed_nodes_forward:
                continue
            curr_estimated_cost = self.open_nodes_forward.get_priority(child)
            child_estimated_cost = child.cost + self.forward_heuristic.estimate_cost(child.board)
            if curr_estimated_cost is None or curr_estimated_cost > child_estimated_cost:
                self.open_nodes_forward.push(child, child_estimated_cost)
        self.closed_nodes_forward.add(node)

    def _backward_step(self):
        node = self.open_nodes_backward.pop()
        if node.board == self.init_board:
            self._finalize(path=node.path())
        elif node in self.closed_nodes_forward:
            # TODO
            forward_node = self.closed_nodes_forward.get(node)
            self._finalize(path=forward_node.path().concatenate(node.path()))

        for child in node.children(shuffle=self.las_vegas_randomization):
            if child in self.closed_nodes_backward:
                continue
            curr_estimated_cost = self.open_nodes_backward.get_priority(child)
            child_estimated_cost = child.cost + self.backward_heuristic.estimate_cost(child.board)
            if curr_estimated_cost is None or curr_estimated_cost > child_estimated_cost:
                self.open_nodes_backward.push(child, child_estimated_cost)
        self.closed_nodes_backward.add(node)

    def _finalize(self, path):
        n_expanded = len(self.closed_nodes_forward) + len(self.closed_nodes_backward) + 1

        self.path = path
        self.results[ResultType.SOLUTION_COST.name] = len(self.path) - 1
        self.results[ResultType.EXPANDED_NODES.name] = n_expanded
        self.results[ResultType.RUN_TIME.name] = time.time() - self.start_time
        raise _GoalFoundSignal()

    def name(self):
        return "BiDirA*"
