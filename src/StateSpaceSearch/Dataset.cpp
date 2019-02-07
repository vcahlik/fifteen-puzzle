#include <StateSpaceSearch/Algorithms/IDAStar.h>
#include <chrono>
#include <Utils.h>
#include <fstream>
#include "Dataset.h"
#include <csignal>

static bool interrupted = false;

void signalHandler(int signal)
{
    interrupted = true;
}

void generateSolutionsDataset(Heuristic *heuristic, int shuffleCnt) {
    IDAStar search(*heuristic);
    auto file = std::ofstream("../data/datasets/solutions-" + currentTimeStr() + ".csv", std::ios::binary | std::fstream::trunc);

    signal(SIGINT, &signalHandler);
    signal(SIGTERM, &signalHandler);

    for (int i = 0; ; ++i) {
        Board board;
        board.shuffle(shuffleCnt);

        auto startTime = std::chrono::high_resolution_clock::now();
        int cost = search.solve(board);
        auto endTime = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime).count();

        file << board << "," << cost << std::endl;

        infoMessage("Generated solution: cost " + std::to_string(cost) + ", duration: " +
                    std::to_string(duration / 1000.0));

        if ((i + 1) % 100 == 0) {
            infoMessage(std::to_string(i + 1) + " solutions generated.");
        }

        if (interrupted) {
            infoMessage("Interrupted by user.");
            break;
        }
    }

    file.close();
}