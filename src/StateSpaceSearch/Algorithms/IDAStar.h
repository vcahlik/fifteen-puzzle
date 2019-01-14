#ifndef FIFTEEN_PUZZLE_SOLVER_IDASTAR_H
#define FIFTEEN_PUZZLE_SOLVER_IDASTAR_H


#include <Board.h>
#include <StateSpaceSearch/Heuristics/ManhattanDistance.h>

class IDAStar {
public:
    explicit IDAStar(const ManhattanDistance &heuristic);

    const int solve(const Board &board);

private:
    const bool costLimitedDFS(const Board &board, int costLimit) const;

    ManhattanDistance heuristic;

};


#endif //FIFTEEN_PUZZLE_SOLVER_IDASTAR_H
