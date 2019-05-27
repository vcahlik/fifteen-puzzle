from prototype.board import Board
from prototype.heuristics.manhattan_distance_heuristic import ManhattanDistanceHeuristic
from prototype.heuristics.pattern_database_heuristic import PatternDatabaseHeuristic
from prototype.heuristics.cpp_pdb_heuristic import CppPatternDatabaseHeuristic


def test_heuristics():
    manhattan = ManhattanDistanceHeuristic(4)
    pdb = PatternDatabaseHeuristic(5)
    cpp_pdb = CppPatternDatabaseHeuristic(5)

    pdb.load_db()
    cpp_pdb.load_db()

    for _ in range(0, 1000):
        board = Board(4)
        board.randomize()
        manhattan_cost = manhattan.estimate_cost(board)
        pdb_cost = pdb.estimate_cost(board)
        cpp_pdb_cost = cpp_pdb.estimate_cost(board)
        assert pdb_cost == cpp_pdb_cost
        assert manhattan_cost <= pdb_cost
