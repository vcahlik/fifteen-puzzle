#ifndef FIFTEEN_PUZZLE_SOLVER_HEURISTIC_H
#define FIFTEEN_PUZZLE_SOLVER_HEURISTIC_H


#include "Board.h"

/**
 * The base class for all heuristic functions.
 */
class Heuristic {
public:
    /**
     * Estimates the optimal solution cost of the specified board.
     */
    virtual int estimateCost(const Board &board) const = 0;

    virtual std::string name() const = 0;
};


#endif //FIFTEEN_PUZZLE_SOLVER_HEURISTIC_H
