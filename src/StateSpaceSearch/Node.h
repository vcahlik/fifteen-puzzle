#ifndef FIFTEEN_PUZZLE_SOLVER_NODE_H
#define FIFTEEN_PUZZLE_SOLVER_NODE_H


#include <memory>
#include <list>
#include "Board.h"

class Node {
public:
    explicit Node(Board board);

    Node(Board board, const Node *parent, Board::Direction lastMoveDirection);

    std::vector<Node> getChildren() const;

    std::list<Node> getPath() const;

    int getCost() const;

    const Board &getBoard() const;

    bool operator==(const Node &other) const;

    bool operator!=(const Node &other) const;

private:
    Board board;
    const Node *parent;
    Board::Direction lastMoveDirection;
    int cost;

};


#endif //FIFTEEN_PUZZLE_SOLVER_NODE_H
