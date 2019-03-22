#ifndef FIFTEEN_PUZZLE_SOLVER_IDASTAR_H
#define FIFTEEN_PUZZLE_SOLVER_IDASTAR_H


#include "Board.h"
#include "StateSpaceSearch/Heuristics/ManhattanDistance.h"

class IDAStar {
public:
    explicit IDAStar(const Heuristic &heuristic);

    int solve(const Board &board) const;

private:
    bool costLimitedDFS(const Board &board, int costLimit) const;

    const Heuristic &heuristic;

};


#endif //FIFTEEN_PUZZLE_SOLVER_IDASTAR_H
