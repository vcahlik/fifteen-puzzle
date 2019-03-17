#include "Board.h"
#include "Utils.h"
#include <StateSpaceSearch/Heuristics/ManhattanDistance.h>
#include <StateSpaceSearch/Heuristics/PatternDatabase.h>
#include <StateSpaceSearch/Benchmark.h>
#include <StateSpaceSearch/Dataset.h>


int main(int argc, char **argv) {
    srand(time(nullptr));

    PatternDatabase pdbh = PatternDatabase(8);
    pdbh.loadDB();
    generateSolutionsDataset(&pdbh, 10000, 10001);

    return EXIT_SUCCESS;
}