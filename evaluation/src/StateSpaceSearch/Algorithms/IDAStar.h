#ifndef FIFTEEN_PUZZLE_SOLVER_IDASTAR_H
#define FIFTEEN_PUZZLE_SOLVER_IDASTAR_H


#include "Board.h"
#include "StateSpaceSearch/Heuristics/ManhattanDistance.h"

/**
 * The iterative deepening A* search algorithm.
 */
class IDAStar {
public:
    explicit IDAStar(const Heuristic &heuristic);

    /**
     * Solves the specified board.
     */
    int solve(const Board &board) const;

private:
    /**
     * Runs the cost limited DFS with the current cost limit.
     */
    bool costLimitedDFS(const Board &board, int costLimit) const;

    const Heuristic &heuristic;

};


#endif //FIFTEEN_PUZZLE_SOLVER_IDASTAR_H
