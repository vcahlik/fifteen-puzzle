from prototype.board import Board
from prototype.utils import Multiset
import pytest


class ClassA:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return self.value


class ClassB:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return self.value


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

    objectA = ClassA(42)
    multiset.insert(objectA)
    assert multiset.get(ClassB(42)) is objectA

    print("success")


# test_multiset()
