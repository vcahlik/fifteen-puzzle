from board import Board
from exceptions import GoalNotFoundError
import custom_queue


def breadth_first_search(init_node, goal_test=Board.is_solved, las_vegas_randomization=False):
    open_nodes = custom_queue.FastLookupQueue()
    open_nodes.push_right(init_node)
    closed_nodes = set()

    while len(open_nodes) > 0:
        node = open_nodes.pop_left()
        if goal_test(node.board):
            return node.path(), len(closed_nodes) + 1
        for child in node.children(shuffle=las_vegas_randomization):
            if (child not in open_nodes) and (child not in closed_nodes):
                open_nodes.push_right(child)
        closed_nodes.add(node)

    raise GoalNotFoundError()
