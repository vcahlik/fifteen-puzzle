#include <algorithm>
#include <StateSpaceSearch/Node.h>
#include <queue>
#include <iostream>
#include <Utils.h>
#include <sstream>
#include <unordered_set>
#include "PatternDatabase.h"

PatternDatabase::PatternDatabase(int maxPatternLength) {
    auto patternsDefinition = getPatternsDefinition(maxPatternLength);
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

std::string PatternDatabase::name() const {
    return "Pattern database heuristic";
}

void PatternDatabase::preCalculate() {
    debugPrint("Database precalculation started.");

    for (auto &subproblem : subproblems) {
        subproblem.preCalculate();
    }

    debugPrint("Database precalculation complete.");
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

int PatternDatabase::Database::size() const {
    int size = 1;
    for (int placementsCnt = 17 - pebblesCnt; placementsCnt < 17; ++placementsCnt) {
        size = size * placementsCnt;
    }
    return size;
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

void PatternDatabase::Database::calculateIndexCoefficients() {
    int c = 1;
    for (int i = 17 - pebblesCnt; i < 17; ++i) {
        indexCoefficients.push_back(c);
        c = c * i;
    }
    std::reverse(indexCoefficients.begin(), indexCoefficients.end());
}

PatternDatabase::Subproblem::Subproblem(std::vector<int> pebbles)
    :   pebbles(pebbles),
        database(static_cast<int>(pebbles.size() + 1)) {

}

int PatternDatabase::Subproblem::estimateCost(const Board &board) const {
    return database.cost(board.getPebblePositionsWithBlank(pebbles));
}

void PatternDatabase::Subproblem::preCalculate() {
    auto hash = [] (const std::shared_ptr<PreCalculationNode> &elem) -> size_t {
        return elem->getBoard().hash();
    };

    auto equal = [] (const std::shared_ptr<PreCalculationNode> &lhs, const std::shared_ptr<PreCalculationNode> &rhs) {
        return *lhs == *rhs;
    };

    auto openQueue = std::queue<std::shared_ptr<PreCalculationNode>>();
    auto openSet = std::unordered_set<std::shared_ptr<PreCalculationNode>, decltype(hash), decltype(equal)>(1000, hash, equal);
    auto closed = std::unordered_set<std::shared_ptr<PreCalculationNode>, decltype(hash), decltype(equal)>(1000, hash, equal);

    auto initNode = std::make_shared<PreCalculationNode>(PartialBoard(pebbles));
    openQueue.push(initNode);
    openSet.insert(initNode);

    while (!openQueue.empty()) {
        auto expansionQueue = std::queue<std::shared_ptr<PreCalculationNode>>();
        auto expansionSet = std::unordered_set<std::shared_ptr<PreCalculationNode>, decltype(hash), decltype(equal)>(50, hash, equal);
        auto popped = openQueue.front();
        expansionQueue.push(popped);
        expansionSet.insert(popped);
        openQueue.pop();
        openSet.erase(popped);

        while (!expansionQueue.empty()) {
            auto node = expansionQueue.front();
            database.saveCost(node->getBoard().getPebblePositionsWithBlank(pebbles), node->getCost());
            expansionQueue.pop();
            expansionSet.erase(node);
            closed.insert(node);

            for (Board::Direction direction : node->getBoard().getValidDirections()) {
                if (node->getLastMoveDirection() == Board::getOppositeDirection(direction)) {
                    continue;
                }

                auto childBoard = PartialBoard(node->getBoard());
                int movedPebble = childBoard.moveBlank(direction);
                auto child = std::make_shared<PreCalculationNode>(childBoard, direction, node->getCost());
                if ((expansionSet.count(child) == 0)
                        && (openSet.count(child) == 0)
                        && (closed.count(child) == 0)) {
                    if (std::find(pebbles.begin(), pebbles.end(), movedPebble) != pebbles.end()) {
                        child->setCost(child->getCost() + 1);
                        openQueue.push(child);
                        openSet.insert(child);
                    } else {
                        expansionQueue.push(child);
                        expansionSet.insert(child);
                    }
                }
            }
        }
    }

    debugPrint(this->name() + " done.");
}

std::string PatternDatabase::Subproblem::name() const {
    std::ostringstream oss;
    oss << "Subproblem {";

    auto first = true;
    for (auto pebble : pebbles) {
        if (first) {
            oss << pebble;
            first = false;
        } else {
            oss << ", " << pebble;
        }
    }

    oss << "}";
    return oss.str();
}

PatternDatabase::Subproblem::PartialBoard::PartialBoard(const std::vector<int> &validPebbles) {
    for (int i = 0; i < solvedPebbles.size(); ++i) {
        int pebble = solvedPebbles[i];
        if (pebble == 0 || std::find(validPebbles.begin(), validPebbles.end(), pebble) != validPebbles.end()) {
            // Pebble is valid (or zero)
            pebbles[i] = pebble;
            pebblePositions[pebble] = i;
        } else {
            pebbles[i] = IGNORED;
            pebblePositions[pebble] = IGNORED;
        }
    }
}

std::array<PebbleIndex, 16> PatternDatabase::Subproblem::PartialBoard::getPebbleIndexes() const {
    throw std::runtime_error("Not implemented yet");
}

bool PatternDatabase::Subproblem::PartialBoard::isSolved() const {
    throw std::runtime_error("Not implemented yet");
}

void PatternDatabase::Subproblem::PartialBoard::setPebblePosition(int pebble, int position) {
    if (pebble != IGNORED && pebblePositions[pebble] != IGNORED) {
        pebblePositions[pebble] = position;
    }
}

PatternDatabase::Subproblem::PreCalculationNode::PreCalculationNode(PartialBoard board, Board::Direction lastMoveDirection, int cost)
    :   board(std::move(board)),
        lastMoveDirection(lastMoveDirection),
        cost(cost) {}

int PatternDatabase::Subproblem::PreCalculationNode::getCost() const {
    return cost;
}

void PatternDatabase::Subproblem::PreCalculationNode::setCost(int cost) {
    this->cost = cost;
}

const PatternDatabase::Subproblem::PartialBoard &PatternDatabase::Subproblem::PreCalculationNode::getBoard() const {
    return board;
}

Board::Direction PatternDatabase::Subproblem::PreCalculationNode::getLastMoveDirection() const {
    return lastMoveDirection;
}

bool PatternDatabase::Subproblem::PreCalculationNode::operator==(const PreCalculationNode &other) const {
    return board == other.board;
}

bool PatternDatabase::Subproblem::PreCalculationNode::operator!=(const PreCalculationNode &other) const {
    return !(*this == other);
}

std::set<std::vector<int>> PatternDatabase::getPatternsDefinition(int maxLen) {
    switch (maxLen) {
        case 1:
            return {{1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}};
        case 2:
            return {{1, 2},
                    {3, 4},
                    {4, 5},
                    {6, 7},
                    {8, 9},
                    {9, 10},
                    {11, 12},
                    {13, 14},
                    {15}};
        case 3:
            return {{1, 2, 5},
                    {3, 4, 8},
                    {6, 9, 10},
                    {7, 11, 12},
                    {13, 14, 15}};
        case 4:
            return {{1, 2, 5, 6},
                    {3, 4, 7, 8},
                    {9, 10, 13, 14},
                    {11, 12, 15}};
        case 5:
            return {{1, 2, 3, 5, 6},
                    {4, 7, 8, 11, 12},
                    {9, 10, 13, 14, 15}};
        case 6:
            return {{1, 2, 5, 6, 9, 10},
                    {3, 4, 7, 8, 11, 12},
                    {13, 14, 15}};
        default:
            throw std::invalid_argument("Not implemented yet.");
    }
}
