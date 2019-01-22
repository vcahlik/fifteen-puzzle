#include "Node.h"

Node::Node(Board board)
        :   board(board),
            parent(nullptr),
            lastMoveDirection(Board::Direction::None) {
    cost = 0;
}

Node::Node(Board board, const Node *parent, Board::Direction lastMoveDirection)
    :   board(board),
        parent(parent),
        lastMoveDirection(lastMoveDirection) {
    cost = parent->cost + 1;
}

std::vector<std::shared_ptr<Node>> Node::getChildren() const {
    auto children = std::vector<std::shared_ptr<Node>>();

    for (Board::Direction direction : this->board.getValidDirections()) {
        if (this->lastMoveDirection != Board::getOppositeDirection(direction)) {
            Board childBoard = Board(board);
            childBoard.moveBlank(direction);
            children.emplace_back(std::make_shared<Node>(childBoard, this, direction));
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

bool Node::operator==(const Node &other) const {
    return board == other.board;
}

bool Node::operator!=(const Node &other) const {
    return !(*this == other);
}
