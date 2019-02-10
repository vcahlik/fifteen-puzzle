#ifndef FIFTEEN_PUZZLE_SOLVER_MANHATTANDISTANCE_H
#define FIFTEEN_PUZZLE_SOLVER_MANHATTANDISTANCE_H


#include <array>
#include "Board.h"
#include "Heuristic.h"

class ManhattanDistance : public Heuristic {
public:
    ManhattanDistance();

    int estimateCost(const Board &board) const override;

    std::string name() const override;

private:
    std::array<PebbleIndex, 16> solvedPebbleIndexes;
};


#endif //FIFTEEN_PUZZLE_SOLVER_MANHATTANDISTANCE_H