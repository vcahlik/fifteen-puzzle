from prototype.board import Board
from prototype.utils import Multiset
import pytest


def test_multiset():
    board1 = Board(4)
    board1.shuffle(10)
    board2 = Board(4)
    board2.shuffle(10)
    multiset = Multiset()

    multiset.insert(board1)
    multiset.insert(board2)
    multiset.insert(board2)

    assert board1 in multiset
    assert board2 in multiset

    multiset.remove(board2)
    assert board2 in multiset
    multiset.remove(board2)
    assert board2 not in multiset

    multiset.remove(board1)
    assert board1 not in multiset
    with pytest.raises(KeyError):
        multiset.remove(board1)

    print("success")


# test_multiset()
