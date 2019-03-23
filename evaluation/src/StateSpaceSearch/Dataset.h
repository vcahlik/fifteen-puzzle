#ifndef FIFTEEN_PUZZLE_SOLVER_DATASET_H
#define FIFTEEN_PUZZLE_SOLVER_DATASET_H


#include "StateSpaceSearch/Heuristics/Heuristic.h"

void generateSolutionsDataset(Heuristic *heuristic, int minShuffleCnt=0, int maxShuffleCount=1000);


#endif //FIFTEEN_PUZZLE_SOLVER_DATASET_H
