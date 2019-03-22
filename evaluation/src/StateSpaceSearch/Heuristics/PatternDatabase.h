#ifndef FIFTEEN_PUZZLE_SOLVER_PATTERNDATABASE_H
#define FIFTEEN_PUZZLE_SOLVER_PATTERNDATABASE_H


#include "Heuristic.h"
#include <set>
#include <list>
#include <cstddef>
#include <memory>

class PatternDatabase : public Heuristic {
public:
    explicit PatternDatabase(int maxPatternLength);

    int estimateCost(const Board &board) const override;

    std::string name() const override;

    void preCalculate();

    void loadDB();

private:
    class Database {
    public:
        explicit Database(int pebblesCnt);

        ~Database();

        Database(const Database &other) = delete;

        Database &operator=(const Database &other) = delete;

        int cost(const std::vector<int> &pebblePositions) const;

        bool hasCost(const std::vector<int> &pebblePositions) const;

        void saveCost(const std::vector<int> &pebblePositions, int cost);

        void clear();

        size_t getSize() const;

        std::byte *getData();

    private:
        size_t index(const std::vector<int> &pebblePositions) const;

        void calculateSize();

        void calculateIndexCoefficients();

        static const std::byte UNSET = static_cast<std::byte>(255);

        size_t size;
        std::byte *data;
        std::vector<size_t> indexCoefficients;
        const int pebblesCnt;
    };

    class Subproblem {
    public:
        explicit Subproblem(std::vector<int> pebbles);

        int estimateCost(const Board &board) const;

        void preCalculate();

        std::string name() const;

        void loadDB();

        void saveDB();

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

        std::string databaseFileName() const;

        const std::vector<int> pebbles;
        Database database;

    };

    static std::set<std::vector<int>> getPatternsDefinition(int maxLen);

    std::list<Subproblem> subproblems;

};


#endif //FIFTEEN_PUZZLE_SOLVER_PATTERNDATABASE_H
