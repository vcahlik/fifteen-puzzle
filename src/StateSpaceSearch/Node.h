#ifndef FIFTEEN_PUZZLE_SOLVER_NODE_H
#define FIFTEEN_PUZZLE_SOLVER_NODE_H


#include <memory>
#include <list>
#include "Board.h"

class Node {
public:
    explicit Node(Board board);

    Node(Board board, const Node *parent, Board::Direction lastMoveDirection, int cost);

    std::vector<std::shared_ptr<Node>> getChildren() const;

    std::list<Node> getPath() const;

    int getCost() const;

    void setCost(int cost);

    const Board &getBoard() const;

    Board::Direction getLastMoveDirection() const;

    bool operator==(const Node &other) const;

    bool operator!=(const Node &other) const;

private:
    Board board;
    const Node *parent;
    Board::Direction lastMoveDirection;
    int cost;

};


#endif //FIFTEEN_PUZZLE_SOLVER_NODE_H
