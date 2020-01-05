import numpy as np
from prototype.board import Board
from prototype.path import Path


class Node:
    """
    A node of a search algorithm.
    """
    def __init__(self, board):
        self.board = board

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(self.board)


class ForwardSearchNode(Node):
    """
    A node for forward search algorithms (most search algorithms are forward).
    """
    def __init__(self, board, parent=None, last_move_direction=None):
        super().__init__(board)
        self.parent = parent
        if parent is not None:
            self.cost = parent.cost + 1
        else:
            self.cost = 0
        self.last_move_direction = last_move_direction

    def children(self, shuffle):
        """
        Returns all child nodes of a node.
        """
        children = []
        for direction in self.board.valid_directions():
            if direction.opposite() != self.last_move_direction:
                child_board = Board(N=self.board.N, config=self.board.config)
                child_board.move_blank(direction)
                children.append(ForwardSearchNode(child_board, self, direction))

        if len(children) > 1 and shuffle:
            np.random.shuffle(children)
        return children

    def path(self):
        """
        Returns a path to the node from the initial state.
        """
        path = Path()
        curr_node = self

        while curr_node is not None:
            path.append(curr_node.board)
            curr_node = curr_node.parent

        return reversed(path)


class BackwardSearchNode(Node):
    """
    A node for backward search algorithms (for example, part of bidirectional search).
    """
    def __init__(self, board, parent=None, last_move_direction=None):
        super().__init__(board)
        self.parent = parent
        if parent is not None:
            self.cost = parent.cost + 1
        else:
            self.cost = 0
        self.last_move_direction = last_move_direction

    def children(self, shuffle):
        """
        Returns all child nodes of a node.
        """
        children = []
        for direction in self.board.valid_directions():
            if direction.opposite() != self.last_move_direction:
                child_board = Board(N=self.board.N, config=self.board.config)
                child_board.move_blank(direction)
                children.append(BackwardSearchNode(child_board, self, direction))

        if len(children) > 1 and shuffle:
            np.random.shuffle(children)
        return children

    def path(self):
        """
        Returns a path to the node from the initial state.
        """
        path = Path()
        curr_node = self

        while curr_node is not None:
            path.append(curr_node.board)
            curr_node = curr_node.parent

        return path
