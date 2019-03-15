from board import Board
from exceptions import GoalNotFoundError
from prototype.graph_search.graph_search_algorithm import GraphSearchAlgorithm
import custom_queue


class BreadthFirstSearch(GraphSearchAlgorithm):
    def __init__(self, goal_test=Board.is_solved, metric=None, las_vegas_randomization=False):
        super().__init__(goal_test, metric)
        self.las_vegas_randomization = las_vegas_randomization

    def run(self, init_node):
        open_nodes = custom_queue.FastLookupQueue()
        open_nodes.push_right(init_node)
        closed_nodes = set()

        while len(open_nodes) > 0:
            node = open_nodes.pop_left()
            if self.goal_test(node.board):
                return node.path(), len(closed_nodes) + 1
            for child in node.children(shuffle=self.las_vegas_randomization):
                if (child not in open_nodes) and (child not in closed_nodes):
                    open_nodes.push_right(child)
            closed_nodes.add(node)

        raise GoalNotFoundError()
