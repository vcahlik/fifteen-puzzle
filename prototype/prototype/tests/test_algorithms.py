from prototype.board import Board
from prototype.graph_search.search_algorithms import BFS, AStarSearch, IDAStarSearch
from prototype.graph_search.node import ForwardSearchNode
from prototype.heuristics.manhattan_distance_heuristic import ManhattanDistanceHeuristic


# Solution costs:  29 ,  35
# Path lengths:  30 ,  36
# [[ 5  7  8  3]
#  [ 1  2  0  4]
#  [ 9  6 11 15]
#  [13 10 12 14]]
# array('l', [5, 7, 8, 3, 1, 2, 0, 4, 9, 6, 11, 15, 13, 10, 12, 14])


def test_algorithms():
    h = ManhattanDistanceHeuristic(4)
    a_star = AStarSearch(h)
    ida_star = IDAStarSearch(h)
    for i in range(0, 20):
        board = Board(N=4)
        board.shuffle(30)
        a_star.run(ForwardSearchNode(board))
        ida_star.run(ForwardSearchNode(board))
        assert a_star.results["SOLUTION_COST"] == ida_star.results["SOLUTION_COST"]
    print("success")


# test_algorithms()
