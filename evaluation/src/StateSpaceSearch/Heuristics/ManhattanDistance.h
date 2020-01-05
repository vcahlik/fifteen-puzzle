#ifndef FIFTEEN_PUZZLE_SOLVER_MANHATTANDISTANCE_H
#define FIFTEEN_PUZZLE_SOLVER_MANHATTANDISTANCE_H


#include "Board.h"
#include "Heuristic.h"
#include <array>

/**
 * The Manhattan distance (MD) heuristic.
 */
class ManhattanDistance : public Heuristic {
public:
    ManhattanDistance();

    /**
     * Estimates the optimal solution cost of the specified board.
     */
    int estimateCost(const Board &board) const override;

    std::string name() const override;

private:
    std::array<PebbleIndex, 16> solvedPebbleIndexes;
};


#endif //FIFTEEN_PUZZLE_SOLVER_MANHATTANDISTANCE_H
