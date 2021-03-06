#include "Node.h"

Node::Node(Board board)
        :   board(std::move(board)),
            parent(nullptr),
            lastMoveDirection(Board::Direction::None) {
    cost = 0;
}

Node::Node(Board board, const Node *parent, Board::Direction lastMoveDirection, int cost)
    :   board(std::move(board)),
        parent(parent),
        lastMoveDirection(lastMoveDirection),
        cost(cost) {}

std::vector<std::shared_ptr<Node>> Node::getChildren() const {
    auto children = std::vector<std::shared_ptr<Node>>();
    children.reserve(3);

    for (Board::Direction direction : this->board.getValidDirections()) {
        if (this->lastMoveDirection != Board::getOppositeDirection(direction)) {
            auto childBoard = Board(board);
            childBoard.moveBlank(direction);
            children.emplace_back(std::make_shared<Node>(std::move(childBoard), this, direction, cost + 1));
        }
    }

    // TODO shuffle

    return children;
}

std::list<Node> Node::getPath() const {
    // TODO
    return std::list<Node>();
}

int Node::getCost() const {
    return cost;
}

const Board &Node::getBoard() const {
    return board;
}

Board::Direction Node::getLastMoveDirection() const {
    return lastMoveDirection;
}

bool Node::operator==(const Node &other) const {
    return board == other.board;
}

bool Node::operator!=(const Node &other) const {
    return !(*this == other);
}
