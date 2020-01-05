#ifndef FIFTEEN_PUZZLE_SOLVER_PATTERNDATABASE_H
#define FIFTEEN_PUZZLE_SOLVER_PATTERNDATABASE_H


#include "Heuristic.h"
#include <set>
#include <list>
#include <cstddef>
#include <memory>

/**
 * The pattern database heuristic.
 */
class PatternDatabase : public Heuristic {
public:
    explicit PatternDatabase(int maxPatternLength);

    /**
     * Estimates the optimal solution cost of the specified board.
     */
    int estimateCost(const Board &board) const override;

    std::string name() const override;

    /**
     * Calculates the pattern databases of the subproblems.
     */
    void preCalculate();

    /**
     * Loads the subproblems' pattern databases from disk.
     */
    void loadDB();

private:
    /**
     * Class representing the pattern database of a subproblem.
     */
    class Database {
    public:
        explicit Database(int pebblesCnt);

        ~Database();

        Database(const Database &other) = delete;

        Database &operator=(const Database &other) = delete;

        /**
         * Returns the cost of a specific subproblem from the database.
         */
        int cost(const std::vector<int> &pebblePositions) const;

        /**
         * Determines whether the cost of a specific subproblem is in the database.
         */
        bool hasCost(const std::vector<int> &pebblePositions) const;

        /**
         * Saves the cost into the database.
         */
        void saveCost(const std::vector<int> &pebblePositions, int cost);

        /**
         * Clears the database.
         */
        void clear();

        /**
         * Returns the size of the database in bytes.
         */
        size_t getSize() const;

        /**
         * Returns the raw memory of the database.
         */
        std::byte *getData();

    private:
        size_t index(const std::vector<int> &pebblePositions) const;

        /**
         * Calculate the size of the database.
         */
        void calculateSize();

        /**
         * Calculates the coefficients to mulitply the positions with to get the "index" (=key) to the database.
         */
        void calculateIndexCoefficients();

        static const std::byte UNSET = static_cast<std::byte>(255);

        size_t size;
        std::byte *data;
        std::vector<size_t> indexCoefficients;
        const int pebblesCnt;
    };

    /**
     * Class representing a subproblem of placing a subset of pebbles to their goal positions.
     */
    class Subproblem {
    public:
        explicit Subproblem(std::vector<int> pebbles);

        /**
         * Returns the optimal solution cost of the subproblem for a given board.
         */
        int estimateCost(const Board &board) const;

        /**
         * Calculates the database of the subproblem.
         */
        void preCalculate();

        std::string name() const;

        /**
         * Loads the database from disk.
         */
        void loadDB();

        /**
         * Saves the database to disk.
         */
        void saveDB();

    private:
        /**
         * A board which ignores some of the pebbles. Used in the subproblems.
         */
        class PartialBoard : public Board {
        public:
            explicit PartialBoard(const std::vector<int> &validPebbles);

            /**
             * Returns the indexes of the pebbles.
             */
            std::array<PebbleIndex, 16> getPebbleIndexes() const override;

            /**
             * Determines whether the board is in the solved configuration.
             */
            bool isSolved() const override;

        protected:
            void setPebblePosition(int pebble, int position) override;

            const int IGNORED = -1;
        };

        /**
         * The search node used in the precalculation of the database.
         */
        class PreCalculationNode {
        public:
            explicit PreCalculationNode(PartialBoard board, Board::Direction lastMoveDirection = Board::Direction::None, int cost = 0);

            /**
             * Returns the cost of the node.
             */
            int getCost() const;

            /**
             * Sets the cost of the node.
             */
            void setCost(int cost);

            /**
             * Returns the board corresponding to the node.
             */
            const PartialBoard &getBoard() const;

            /**
             * Returns the direction of the last move.
             */
            Board::Direction getLastMoveDirection() const;

            bool operator==(const PreCalculationNode &other) const;

            bool operator!=(const PreCalculationNode &other) const;

        private:
            PartialBoard board;
            Board::Direction lastMoveDirection;
            int cost;
        };

        /**
         * Returns the filename of the database file.
         */
        std::string databaseFileName() const;

        const std::vector<int> pebbles;
        Database database;

    };

    /**
     * Returns the subproblem pattern definitions for the specified max length of a subproblem.
     */
    static std::set<std::vector<int>> getPatternsDefinition(int maxLen);

    std::list<Subproblem> subproblems;

};


#endif //FIFTEEN_PUZZLE_SOLVER_PATTERNDATABASE_H
