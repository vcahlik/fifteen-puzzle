#include <chrono>
#include <StateSpaceSearch/Algorithms/IDAStar.h>
#include <iostream>
#include <Utils.h>
#include "Benchmark.h"

void randomSolveBenchmark(std::list<Heuristic *> heuristics, int shuffleCnt, int runsCnt) {
    for (int i = 0; (runsCnt < 0) || (i < runsCnt); ++i) {
        Board board;
        board.shuffle(shuffleCnt);

        for (auto &heuristic : heuristics) {
            IDAStar search(*heuristic);
            auto startTime = std::chrono::high_resolution_clock::now();
            int cost = search.solve(board);
            auto endTime = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime).count();

            infoMessage(heuristic->name() + ": cost " + std::to_string(cost) + ", duration: " +
                        std::to_string(duration / 1000.0));
        }
    }
}

void boardShufflingBenchmark(int shuffleCnt, int runsCnt) {
    auto startTime = std::chrono::high_resolution_clock::now();

    for (int i = 0; (runsCnt < 0) || (i < runsCnt); ++i) {
        Board board;
        board.shuffle(shuffleCnt);
    }

    auto endTime = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime).count();

    infoMessage("Board shuffling benchmark duration: " + std::to_string(duration / 1000.0));
}

void heuristicsBenchmark(std::list<Heuristic *> heuristics, int shuffleCnt, int runsCnt) {
    ManhattanDistance mh;

    for (int i = 0; (runsCnt < 0) || (i < runsCnt); ++i) {
        Board board;
        board.shuffle(shuffleCnt);

        for (auto &heuristic : heuristics) {
            int cost = heuristic->estimateCost(board);
            infoMessage(heuristic->name() + ": cost " + std::to_string(cost));
        }

        IDAStar search(mh);
        infoMessage("Real cost:" + std::to_string(search.solve(board)));
    }
}