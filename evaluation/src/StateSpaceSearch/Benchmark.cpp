#include "Benchmark.h"
#include "StateSpaceSearch/Algorithms/IDAStar.h"
#include "Utils.h"
#include <chrono>
#include <iostream>

void randomSolveBenchmark(std::list<Heuristic *> heuristics, int shuffleCnt, int runsCnt) {
    for (int i = 0; (runsCnt < 0) || (i < runsCnt); ++i) {
        Board board;
        board.shuffle(shuffleCnt);

        int lastCost = -1;
        for (auto &heuristic : heuristics) {
            IDAStar search(*heuristic);
            auto startTime = std::chrono::high_resolution_clock::now();
            int cost = search.solve(board);
            auto endTime = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime).count();

            infoMessage(heuristic->name() + ": cost " + std::to_string(cost) + ", duration: " +
                        std::to_string(duration / 1000.0));

            if (lastCost >= 0 && lastCost != cost) {
                throw std::runtime_error("Optimal solutions not equal");
            }
            lastCost = cost;
        }

        if ((i + 1) % 100 == 0) {
            infoMessage("Random solve benchmark: " + std::to_string(i + 1) + " boards solved.");
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
    for (int i = 0; (runsCnt < 0) || (i < runsCnt); ++i) {
        Board board;
        board.shuffle(shuffleCnt);

        for (auto &heuristic : heuristics) {
            int cost = heuristic->estimateCost(board);
            infoMessage(heuristic->name() + ": cost " + std::to_string(cost));
        }

        IDAStar search(**heuristics.begin());
        infoMessage("Real cost:" + std::to_string(search.solve(board)));
    }
}