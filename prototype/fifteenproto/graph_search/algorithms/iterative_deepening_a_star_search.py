from board import Board
from exceptions import GoalNotFoundError
import custom_queue


def cost_limited_depth_first_search(init_node, heuristic, cost_limit, goal_test=Board.is_solved, las_vegas_randomization=False):
    open_nodes = custom_queue.FastLookupQueue()
    open_nodes.push_right(init_node)
    n_explored = 0

    while len(open_nodes) > 0:
        node = open_nodes.pop_right()
        n_explored = n_explored + 1
        if goal_test(node.board):
            return node.path(), n_explored
        for child in node.children(shuffle=las_vegas_randomization):
            estimated_cost = child.cost + heuristic.cost(child.board)
            if estimated_cost <= cost_limit:
                open_nodes.push_right(child)

    raise GoalNotFoundError()


def iterative_deepening_a_star_search(init_node, heuristic, goal_test=Board.is_solved, las_vegas_randomization=False):
    cost_limit = heuristic.cost(init_node.board)

    while True:
        try:
            path, expanded_nodes = cost_limited_depth_first_search(init_node, heuristic, cost_limit, goal_test, las_vegas_randomization)
            return path, expanded_nodes
        except GoalNotFoundError:
            cost_limit = cost_limit + 2
            continue
