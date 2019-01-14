#include "Node.h"

Node::Node(Board board)
        :   board(board),
            parent(nullptr) {
    cost = 0;
}

Node::Node(Board board, const Node *parent, Board::Direction lastMoveDirection)
    :   board(std::move(board)),
        parent(parent),
        lastMoveDirection(lastMoveDirection) {
    cost = parent->cost + 1;
}

const std::vector<Node> Node::getChildren() const {
    auto children = std::vector<Node>();

    for (Board::Direction direction : this->board.getValidDirections()) {
        if (this->lastMoveDirection != Board::getOppositeDirection(direction)) {
            Board childBoard = Board(board);
            childBoard.moveBlank(direction);
            children.emplace_back(Node(std::move(childBoard), this, direction));
        }
    }

    // TODO shuffle

    return children;
}

const std::list<Node> Node::getPath() const {
    // TODO
    return std::list<Node>();
}

const int Node::getCost() const {
    return cost;
}

const Board &Node::getBoard() const {
    return board;
}

bool Node::operator==(const Node &other) const {
    return board == other.board;
}

bool Node::operator!=(const Node &other) const {
    return !(*this == other);
}
