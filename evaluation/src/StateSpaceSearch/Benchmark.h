#ifndef FIFTEEN_PUZZLE_SOLVER_BENCHMARK_H
#define FIFTEEN_PUZZLE_SOLVER_BENCHMARK_H


#include "StateSpaceSearch/Heuristics/Heuristic.h"
#include <list>

void randomSolveBenchmark(std::list<Heuristic *> heuristics, int shuffleCnt=5000, int runsCnt=-1);

void boardShufflingBenchmark(int shuffleCnt=5000, int runsCnt=-1);

void heuristicsBenchmark(std::list<Heuristic *> heuristics, int shuffleCnt=5000, int runsCnt=-1);


#endif //FIFTEEN_PUZZLE_SOLVER_BENCHMARK_H
