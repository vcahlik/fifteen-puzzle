#include <iostream>
#include "Board.h"

constexpr std::array<int, 16> Board::solvedPebbles;
constexpr std::array<int, 16> Board::solvedPebblePositions;

PebbleIndex::PebbleIndex(int row, int col)
    :   row(row),
        col(col) {

}

Board::Board()
        :   pebbles(solvedPebbles),
            pebblePositions(solvedPebblePositions) {

}

Board::Board(std::array<int, 16> pebbles)
    :   pebbles(pebbles) {
    calculatePebblePositions();
}

bool Board::isSolved() const {
    return pebbles == Board::solvedPebbles;
}

std::array<PebbleIndex, 16> Board::getPebbleIndexes() const {
    auto pebbleIndexes = std::array<PebbleIndex, 16>();

    for (int i = 0; i < 16; ++i) {
        pebbleIndexes[i] = positionToIndex(pebblePositions[i]);
    }

    return pebbleIndexes;
}

std::vector<Board::Direction> Board::getValidDirections() const {
    auto directions = std::vector<Board::Direction>();
    PebbleIndex indexOfBlank = positionToIndex(pebblePositions[0]);

    if (indexOfBlank.row > 0) {directions.push_back(Direction::Up);}
    if (indexOfBlank.row < 3) {directions.push_back(Direction::Down);}
    if (indexOfBlank.col > 0) {directions.push_back(Direction::Left);}
    if (indexOfBlank.col < 3) {directions.push_back(Direction::Right);}

    return directions;
}

int Board::moveBlank(const Board::Direction direction) {
    int oldBlankPosition = pebblePositions[0];
    int newBlankPosition = oldBlankPosition + getBlankPositionChange(direction);
    int replacedPebble = pebbles[newBlankPosition];

    pebbles[newBlankPosition] = 0;
    pebbles[oldBlankPosition] = replacedPebble;
    pebblePositions[0] = newBlankPosition;
    pebblePositions[replacedPebble] = oldBlankPosition;

    return replacedPebble;
}

void Board::shuffle(int movesCnt) {
    for (int i = 0; i < movesCnt; ++i) {
        auto directions = getValidDirections();
        Direction direction = directions[rand() % directions.size()];
        moveBlank(direction);
    }
}

PebbleIndex Board::positionToIndex(int position) {
    return PebbleIndex(position / 4, position % 4);
}

int Board::getBlankPositionChange(Board::Direction direction) {
    switch (direction) {
        case Direction::Up:
            return -4;
        case Direction::Down:
            return 4;
        case Direction::Left:
            return -1;
        case Direction::Right:
            return 1;
    }
}

Board::Direction Board::getOppositeDirection(Direction direction) {
    switch (direction) {
        case Direction::Up:
            return Direction::Down;
        case Direction::Down:
            return Direction::Up;
        case Direction::Left:
            return Direction::Right;
        case Direction::Right:
            return Direction::Left;
    }
}

void Board::print() {
    std::cout << solvedPebblePositions[0] << std::endl;
}

bool Board::operator==(const Board &other) const {
    return pebbles == other.pebbles;
}

bool Board::operator!=(const Board &other) const {
    return !(*this == other);
}

void Board::calculatePebblePositions() {
    for (int position = 0; position < pebbles.size(); ++position) {
        int pebble = pebbles[position];
        pebblePositions[pebble] = position;
    }
}