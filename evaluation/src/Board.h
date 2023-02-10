#ifndef FIFTEEN_PUZZLE_SOLVER_BOARD_H
#define FIFTEEN_PUZZLE_SOLVER_BOARD_H


#include <vector>
#include <array>
#include <ostream>

/**
 * The index of the pebble position, storing a row and a column.
 */
struct PebbleIndex {
public:
    explicit PebbleIndex(int row = 0, int col = 0);

    int row;
    int col;
};

/**
 * Class representing boards with pebbles.
 */
class Board {
public:
    enum class Direction {
        Up,
        Down,
        Left,
        Right,
        None
    };

    Board();

    explicit Board(std::array<int, 16> pebbles);

    bool operator==(const Board &other) const;

    bool operator!=(const Board &other) const;

    /**
     * Determines whether the board is in a solved state.
     */
    virtual bool isSolved() const;

    /**
     * Returns an array with the indexes of the pebbles.
     */
    virtual std::array<PebbleIndex, 16> getPebbleIndexes() const;

    /**
     * Returns a vector of directions of the currently valid moves.
     */
    const std::vector<Board::Direction> &getValidDirections() const;

    /**
     * Returns a direction opposite to the specified direction.
     */
    static Direction getOppositeDirection(Direction direction);

    /**
     * Returns the positions of the blank and the pebbles.
     */
    std::vector<int> getPebblePositionsWithBlank(std::vector<int> pebbles) const;

    /**
     * Moves the blank in the specified direction.
     */
    int moveBlank(Direction direction);

    /**
     * Randomly shuffles the board.
     * @param minMovesCnt
     * @param randomize Whether to randomly add 1 to the moves count (in order not to always return boards with an even or odd optimal solution cost)
     */
    void shuffle(int minMovesCnt, bool randomize=false);

    /**
     * Calculates the hash of the board using the pebble positions.
     * @return
     */
    std::size_t hash() const;

    friend std::ostream& operator<<(std::ostream& os, const Board& board);

    void print() const;

protected:
    virtual void setPebblePosition(int pebble, int position);

    static constexpr std::array<int, 16> solvedPebbles = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0};
    static constexpr std::array<int, 16> solvedPebblePositions = {15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14};

    std::array<int, 16> pebbles;
    std::array<int, 16> pebblePositions;

private:
    /**
     * Calculates the positions of the pebbles.
     */
    void calculatePebblePositions();

    /**
     * Conerts a pebble position to a pebble index.
     */
    static PebbleIndex positionToIndex(int position);

    /**
     * Calculates the change of the position of the blank after it has been moved in the specified direction.
     */
    static int getBlankPositionChange(Direction direction);

};


#endif //FIFTEEN_PUZZLE_SOLVER_BOARD_H
