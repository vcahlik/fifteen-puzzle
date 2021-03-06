#include "ManhattanDistance.h"

ManhattanDistance::ManhattanDistance() {
    solvedPebbleIndexes = Board().getPebbleIndexes();
}

int ManhattanDistance::estimateCost(const Board &board) const {
    auto pebbleIndexes = board.getPebbleIndexes();
    int cost = 0;

    for (int i = 1; i < pebbleIndexes.size(); ++i) {
        cost += abs(pebbleIndexes[i].col - solvedPebbleIndexes[i].col) + abs(pebbleIndexes[i].row - solvedPebbleIndexes[i].row);
    }

    return cost;
}

std::string ManhattanDistance::name() const {
    return "Manhattan distance heuristic";
}
