#ifndef FIFTEEN_PUZZLE_SOLVER_PATTERNDATABASE_H
#define FIFTEEN_PUZZLE_SOLVER_PATTERNDATABASE_H


#include <set>
#include <list>
#include <cstddef>
#include <memory>
#include "Heuristic.h"

class PatternDatabase : public Heuristic {
public:
    explicit PatternDatabase(int maxPatternLength);

    int estimateCost(const Board &board) const override;

    std::string name() const override;

    void preCalculate();

private:
    class Database {
    public:
        explicit Database(int pebblesCnt);

        ~Database();

        Database(const Database &other) = delete;

        Database &operator=(const Database &other) = delete;

        int cost(const std::vector<int> &pebblePositions) const;

        void saveCost(const std::vector<int> &pebblePositions, int cost);

        int size() const;

    private:
        int index(const std::vector<int> &pebblePositions) const;

        void calculateIndexCoefficients();

        std::byte *data;
        std::vector<int> indexCoefficients;
        const int pebblesCnt;
    };

    class Subproblem {
    public:
        explicit Subproblem(std::vector<int> pebbles);

        int estimateCost(const Board &board) const;

        void preCalculate();

        std::string name() const;

    private:
        class PartialBoard : public Board {
        public:
            explicit PartialBoard(const std::vector<int> &validPebbles);

            std::array<PebbleIndex, 16> getPebbleIndexes() const override;

            bool isSolved() const override;

        protected:
            void setPebblePosition(int pebble, int position) override;

            const int IGNORED = -1;
        };

        class PreCalculationNode {
        public:
            explicit PreCalculationNode(PartialBoard board, Board::Direction lastMoveDirection = Board::Direction::None, int cost = 0);

            int getCost() const;

            void setCost(int cost);

            const PartialBoard &getBoard() const;

            Board::Direction getLastMoveDirection() const;

            bool operator==(const PreCalculationNode &other) const;

            bool operator!=(const PreCalculationNode &other) const;

        private:
            PartialBoard board;
            Board::Direction lastMoveDirection;
            int cost;
        };

        const std::vector<int> pebbles;
        Database database;

    };

    static std::set<std::vector<int>> getPatternsDefinition(int maxLen);

    std::list<Subproblem> subproblems;

};


#endif //FIFTEEN_PUZZLE_SOLVER_PATTERNDATABASE_H
