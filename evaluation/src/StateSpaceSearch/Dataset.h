#ifndef FIFTEEN_PUZZLE_SOLVER_DATASET_H
#define FIFTEEN_PUZZLE_SOLVER_DATASET_H


#include "StateSpaceSearch/Heuristics/Heuristic.h"

/**
 * Generates the CSV with the pebble positions of boards and their corresponding optimal solution costs using IDA*.
 * @param heuristic Heuristic to be used with IDA*
 * @param minShuffleCnt
 * @param maxShuffleCount 
 */
void generateSolutionsDataset(Heuristic *heuristic, int minShuffleCnt=0, int maxShuffleCount=1000);


#endif //FIFTEEN_PUZZLE_SOLVER_DATASET_H
