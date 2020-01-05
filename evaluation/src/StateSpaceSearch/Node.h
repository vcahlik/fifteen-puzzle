#ifndef FIFTEEN_PUZZLE_SOLVER_NODE_H
#define FIFTEEN_PUZZLE_SOLVER_NODE_H


#include "Board.h"
#include <memory>
#include <list>

/**
 * Class representing a search node in a search algorithm.
 */
class Node {
public:
    explicit Node(Board board);

    Node(Board board, const Node *parent, Board::Direction lastMoveDirection, int cost);

    /**
     * Returns a vector of all child nodes of the node.
     */
    std::vector<std::shared_ptr<Node>> getChildren() const;

    /**
     * Returns a path from the initial state to the current state.
     */
    std::list<Node> getPath() const;

    /**
     * Returns the cost of the node.
     */
    int getCost() const;

    /**
     * Returns the board corresponding to the node.
     */
    const Board &getBoard() const;

    /**
     * Returns the direction of the last move.
     */
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
