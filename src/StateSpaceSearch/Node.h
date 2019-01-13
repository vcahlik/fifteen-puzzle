#ifndef FIFTEEN_PUZZLE_SOLVER_NODE_H
#define FIFTEEN_PUZZLE_SOLVER_NODE_H


#include <memory>
#include <list>
#include "Board.h"

class Node {
public:
    Node(std::unique_ptr<Board> board, const Node *parent, Board::Direction lastMoveDirection);

    const std::vector<Node> getChildren() const;

    const std::list<Node> getPath() const;

    const int getCost() const;

    bool operator==(const Node &other) const;

    bool operator!=(const Node &other) const;

private:
    std::unique_ptr<Board> board;
    const Node *parent;
    Board::Direction lastMoveDirection;
    int cost;

};


#endif //FIFTEEN_PUZZLE_SOLVER_NODE_H
