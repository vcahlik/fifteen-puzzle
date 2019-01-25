#include <algorithm>
#include "PatternDatabase.h"

PatternDatabase::PatternDatabase(std::set<std::vector<int>> patternsDefinition) {
    for (const auto &pebbles : patternsDefinition) {
        subproblems.emplace_back(pebbles);
    }
}

int PatternDatabase::estimateCost(const Board &board) const {
    int cost = 0;
    for (const auto &subproblem : subproblems) {
        cost += subproblem.estimateCost(board);
    }
    return cost;
}

PatternDatabase::Database::Database(int pebblesCnt)
    :   pebblesCnt(pebblesCnt) {
    data = new std::byte[size()];
    calculateIndexCoefficients();
}

PatternDatabase::Database::~Database() {
    delete[] data;
}

int PatternDatabase::Database::cost(const std::vector<int> &pebblePositions) const {
    return static_cast<int>(data[index(pebblePositions)]);
}

void PatternDatabase::Database::saveCost(const std::vector<int> &pebblePositions, int cost) {
    data[index(pebblePositions)] = static_cast<std::byte>(cost);
}

int PatternDatabase::Database::index(const std::vector<int> &pebblePositions) const {
    int index = 0;
    std::vector<int> readjustments(pebblesCnt, 0);

    for (int i = 0; i < pebblesCnt; ++i) {
        index += indexCoefficients[i] * (pebblePositions[i] + readjustments[i]);

        for (int j = i + 1; j < pebblesCnt; ++j) {
            if (pebblePositions[j] > pebblePositions[i]) {
                readjustments[j] -= 1;
            }
        }
    }

    return index;
}

int PatternDatabase::Database::size() const {
    int size = 1;
    for (int placementsCnt = 17 - pebblesCnt; placementsCnt < 17; ++placementsCnt) {
        size = size * placementsCnt;
    }
    return size;
}

void PatternDatabase::Database::calculateIndexCoefficients() {
    int c = 1;
    for (int i = 17 - pebblesCnt; i < 17; ++i) {
        indexCoefficients.push_back(c);
        c = c * i;
    }
    std::reverse(indexCoefficients.begin(), indexCoefficients.end());
}

PatternDatabase::Subproblem::Subproblem(std::vector<int> pebbles)
    :   pebbles(std::move(pebbles)),
        database(static_cast<int>(pebbles.size() + 1)) {

}

int PatternDatabase::Subproblem::estimateCost(const Board &board) const {
    //TODO
    return 0;
}
