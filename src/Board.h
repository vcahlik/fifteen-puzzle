#ifndef FIFTEEN_PUZZLE_SOLVER_BOARD_H
#define FIFTEEN_PUZZLE_SOLVER_BOARD_H


#include <vector>
#include <array>

struct PebbleIndex {
public:
    explicit PebbleIndex(int row = 0, int col = 0);

    int row;
    int col;
};

class Board {
public:
    enum class Direction {
        Up,
        Down,
        Left,
        Right
    };

    Board();

    explicit Board(std::array<int, 16> pebbles);

    bool operator==(const Board &other) const;

    bool operator!=(const Board &other) const;

    bool isSolved() const;

    std::array<PebbleIndex, 16> getPebbleIndexes() const;

    std::vector<Board::Direction> getValidDirections() const;

    int moveBlank(Direction direction);

    void shuffle(int movesCnt);

    static PebbleIndex positionToIndex(int position);

    static int getBlankPositionChange(Direction direction);

    static Direction getOppositeDirection(Direction direction);

    void print();

private:
    void calculatePebblePositions();

    std::array<int, 16> pebbles;
    std::array<int, 16> pebblePositions;

    static constexpr std::array<int, 16> solvedPebbles = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0};
    static constexpr std::array<int, 16> solvedPebblePositions = {15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14};

};


#endif //FIFTEEN_PUZZLE_SOLVER_BOARD_H
