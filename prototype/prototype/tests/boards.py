from prototype.board import Board
from prototype.graph_search.search_algorithms import BFS, AStarSearch
from prototype.graph_search.node import ForwardSearchNode

for size in range(2, 6):
    for i in range(0, 10):
        board = Board(N=size)
        board.randomize(enforce_solvability=True)
        assert board.is_solvable(), "Solvability test: failed"

for size in range(2, 4):
    for i in range(0, 5):
        try:
            board = Board(N=size)
            board.randomize(enforce_solvability=True)
            bfs = BFS()
            bfs.run(ForwardSearchNode(board))
        except:
            print("BFS easy test: failed")

for size in range(2, 6):
    for i in range(0, 4):
        try:
            board = Board(N=size)
            board.shuffle(5)
            bfs = BFS()
            bfs.run(ForwardSearchNode(board))
        except:
            print("BFS hard test: failed")

print("All tests succeeded!")
