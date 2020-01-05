#ifndef FIFTEEN_PUZZLE_SOLVER_BENCHMARK_H
#define FIFTEEN_PUZZLE_SOLVER_BENCHMARK_H


#include "StateSpaceSearch/Heuristics/Heuristic.h"
#include <list>

/**
 * A test of solving random boards.
 */
void randomSolveBenchmark(std::list<Heuristic *> heuristics, int shuffleCnt=5000, int runsCnt=-1);

/**
 * A test of random shuffling of the boards.
 */
void boardShufflingBenchmark(int shuffleCnt=5000, int runsCnt=-1);

/**
 * A test of heuristics.
 */
void heuristicsBenchmark(std::list<Heuristic *> heuristics, int shuffleCnt=5000, int runsCnt=-1);


#endif //FIFTEEN_PUZZLE_SOLVER_BENCHMARK_H
