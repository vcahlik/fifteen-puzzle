#ifndef FIFTEEN_PUZZLE_SOLVER_PATTERNDATABASE_H
#define FIFTEEN_PUZZLE_SOLVER_PATTERNDATABASE_H


#include <set>
#include <list>
#include <cstddef>
#include "Heuristic.h"

class PatternDatabase : public Heuristic {
public:
    explicit PatternDatabase(std::set<std::vector<int>> patternsDefinition);

    int estimateCost(const Board &board) const override;

private:
    class Database {
    public:
        explicit Database(int pebblesCnt);

        ~Database();

        Database(const Database &other) = delete;

        Database &operator=(const Database &other) = delete;

        int cost(const std::vector<int> &pebblePositions) const;

        void saveCost(const std::vector<int> &pebblePositions, int cost);

    private:
        int index(const std::vector<int> &pebblePositions) const;

        int size() const;

        void calculateIndexCoefficients();

        std::byte *data;
        std::vector<int> indexCoefficients;
        const int pebblesCnt;
    };

    class Subproblem {
    public:
        explicit Subproblem(std::vector<int> pebbles);

        int estimateCost(const Board &board) const;

    private:
        const std::vector<int> pebbles;
        Database database;

    };

    std::list<Subproblem> subproblems;

};


#endif //FIFTEEN_PUZZLE_SOLVER_PATTERNDATABASE_H
