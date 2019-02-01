#ifndef FIFTEEN_PUZZLE_SOLVER_BENCHMARK_H
#define FIFTEEN_PUZZLE_SOLVER_BENCHMARK_H


#include <list>
#include <StateSpaceSearch/Heuristics/Heuristic.h>

void randomSolveBenchmark(std::list<Heuristic *> heuristics, int shuffleCnt=500, int runsCnt=-1);

void heuristicsBenchmark(std::list<Heuristic *> heuristics, int shuffleCnt=500, int runsCnt=-1);


#endif //FIFTEEN_PUZZLE_SOLVER_BENCHMARK_H
