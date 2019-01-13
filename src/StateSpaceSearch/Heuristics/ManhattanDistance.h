#ifndef FIFTEEN_PUZZLE_SOLVER_MANHATTANDISTANCE_H
#define FIFTEEN_PUZZLE_SOLVER_MANHATTANDISTANCE_H


#include <array>
#include "Board.h"

class ManhattanDistance {
public:
    ManhattanDistance();

    const int estimateCost(const Board &board) const;

private:
    std::array<PebbleIndex, 16> solvedPebbleIndexes;
};


#endif //FIFTEEN_PUZZLE_SOLVER_MANHATTANDISTANCE_H
