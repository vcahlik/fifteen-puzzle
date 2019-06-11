from prototype.board import Board
from prototype.graph_search.search_algorithms import BFS, AStarSearch, IDAStarSearch, BackwardAStarSearch
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
    
    
def test_backward_a_star():
    mdh = ManhattanDistanceHeuristic(4)
    a_star = AStarSearch(mdh)
    backward_mdh = ManhattanDistanceHeuristic(4)
    backward_a_star = BackwardAStarSearch(backward_mdh)
    for i in range(0, 20):
        board = Board(N=4)
        board.shuffle(25)
        a_star.run(board)
        backward_a_star.run(board)
        assert a_star.results["SOLUTION_COST"] == backward_a_star.results["SOLUTION_COST"]
    print("success")

# test_algorithms()
# test_backward_a_star()
