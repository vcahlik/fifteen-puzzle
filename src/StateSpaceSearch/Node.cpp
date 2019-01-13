#include "Node.h"

Node::Node(std::unique_ptr<Board> board, const Node *parent, Board::Direction lastMoveDirection)
    :   board(std::move(board)),
        parent(parent),
        lastMoveDirection(lastMoveDirection) {
    if (parent == nullptr) {
        cost = 0;
    } else {
        cost = parent->cost + 1;
    }
}

const std::vector<Node> Node::getChildren() const {
    auto children = std::vector<Node>();

    for (Board::Direction direction : this->board->getValidDirections()) {
        if (this->lastMoveDirection != Board::getOppositeDirection(direction)) {
            auto childBoard = std::make_unique<Board>(Board(*board));
            childBoard->moveBlank(direction);
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

bool Node::operator==(const Node &other) const {
    return board == other.board;
}

bool Node::operator!=(const Node &other) const {
    return !(*this == other);
}
