from prototype.board import Board
from prototype.graph_search.search_algorithms import BFS, AStarSearch, IDAStarSearch
from prototype.graph_search.node import ForwardSearchNode
from prototype.heuristics.manhattan_distance_heuristic import ManhattanDistanceHeuristic


def test_algorithms():
    h = ManhattanDistanceHeuristic(4)
    a_star = AStarSearch(h)
    ida_star = IDAStarSearch(h)
    for i in range(0, 20):
        board = Board(N=4)
        board.shuffle(25)
        a_star.run(board)
        ida_star.run(board)
        assert a_star.results["SOLUTION_COST"] == ida_star.results["SOLUTION_COST"]
    print("success")


# test_algorithms()
