#ifndef FIFTEEN_PUZZLE_SOLVER_HEURISTIC_H
#define FIFTEEN_PUZZLE_SOLVER_HEURISTIC_H


#include "Board.h"

class Heuristic {
public:
    virtual int estimateCost(const Board &board) const = 0;

    virtual std::string name() const = 0;
};


#endif //FIFTEEN_PUZZLE_SOLVER_HEURISTIC_H
