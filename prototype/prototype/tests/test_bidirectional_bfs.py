from prototype.graph_search.bidirectional_bfs import BidirectionalBFS
from prototype.graph_search.search_algorithms import BFS
from prototype.board import Board


def test_bidirectional_bfs():
    bfs = BFS()
    bidirectional_bfs = BidirectionalBFS()
    for i in range(0, 10):
        board = Board(N=4)
        board.shuffle(10)
        bfs.run(board)
        bidirectional_bfs.run(board)

        assert bfs.results["SOLUTION_COST"] == bidirectional_bfs.results["SOLUTION_COST"]
        bfs.path.check_validity()
        bidirectional_bfs.path.check_validity()
    print("success")


# test_bidirectional_bfs()
