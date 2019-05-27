from prototype.board import Board
from prototype.graph_search.search_algorithms import BFS, AStarSearch, IDAStarSearch
from prototype.graph_search.node import ForwardSearchNode
from prototype.heuristics.pattern_database_heuristic import PatternDatabaseHeuristic
from prototype.heuristics.cpp_pdb_heuristic import CppPatternDatabaseHeuristic
import array


def test_randomize():
    for size in range(2, 6):
        for i in range(0, 10):
            board = Board(N=size)
            board.randomize(enforce_solvability=True)
            assert board.is_solvable()
    print("success")


def test_randomize_bfs():
    for size in range(2, 3):
        for i in range(0, 5):
            board = Board(N=size)
            board.randomize(enforce_solvability=True)
            bfs = BFS()
            bfs.run(board)
    print("success")


def test_shuffle():
    for size in range(2, 6):
        for i in range(0, 10):
            board = Board(N=size)
            board.shuffle(500)
            assert board.is_solvable()
    print("success")


def test_unsolvable():
    for i in range(0, 10):
        board = Board(N=4, config=array.array('l', (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14, 0)))
        board.shuffle(500)
        assert not board.is_solvable()
    print("success")


def test_shuffle_bfs():
    for size in range(2, 6):
        for i in range(0, 10):
            board = Board(N=size)
            board.shuffle(8)
            bfs = BFS()
            bfs.run(board)
    print("success")


def test_pdb_heuristic():
    h = PatternDatabaseHeuristic(5)
    h.load_db()
    search = AStarSearch(h)
    for i in range(0, 10):
        board = Board(N=4)
        board.shuffle(30)
        search.run(board)
    print("success")


def test_cpp_pdb_heuristic():
    h = CppPatternDatabaseHeuristic(5)
    h.load_db()
    search = AStarSearch(h)
    for i in range(0, 10):
        board = Board(N=4)
        board.shuffle(30)
        search.run(board)
    print("success")


# test_randomize()
# test_randomize_bfs()
# test_shuffle()
# test_shuffle_bfs()
# test_pdb_heuristic()
# test_cpp_pdb_heuristic()
