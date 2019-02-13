from custom_queue import PriorityQueue
from board import Board
from exceptions import GoalNotFoundError


def a_star_search(init_node, heuristic, goal_test=Board.is_solved, las_vegas_randomization=False):
    open_nodes = PriorityQueue()
    open_nodes.push(init_node, heuristic.cost(init_node.board))
    closed_nodes = set()

    while len(open_nodes) > 0:
        node = open_nodes.pop()
        if goal_test(node.board):
            return node.path(), len(closed_nodes) + 1
        for child in node.children(shuffle=las_vegas_randomization):
            if child in closed_nodes:
                continue
            curr_estimated_cost = open_nodes.get_priority(child)
            child_estimated_cost = child.cost + heuristic.cost(child.board)
            if curr_estimated_cost is None or curr_estimated_cost > child_estimated_cost:
                open_nodes.push(child, child_estimated_cost)
                closed_nodes.add(node)

    raise GoalNotFoundError()
