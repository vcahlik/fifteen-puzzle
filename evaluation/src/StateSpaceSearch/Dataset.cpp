#include "StateSpaceSearch/Algorithms/IDAStar.h"
#include "Utils.h"
#include "Dataset.h"
#include "Config.h"
#include <chrono>
#include <fstream>
#include <csignal>
#include <random>

static bool interrupted = false;

void signalHandler(int signal)
{
    interrupted = true;
}

void generateSolutionsDataset(Heuristic *heuristic, int minShuffleCnt, int maxShuffleCount) {
    IDAStar search(*heuristic);
    auto file = std::ofstream(Config::Paths::DATASETS_RAW_DIR + "/15-costs/solutions-" + currentTimeStr() + ".csv", std::ios::binary | std::fstream::trunc);
    if (!file) {
        throw std::runtime_error("Can't open output file");
    }

    std::random_device rd;
    std::mt19937 rng(rd());
    std::uniform_int_distribution<int> random_uniform(minShuffleCnt, maxShuffleCount);

    signal(SIGINT, &signalHandler);
    signal(SIGTERM, &signalHandler);

    for (int i = 0; ; ++i) {
        Board board;
        auto shufflesCnt = random_uniform(rng);
        board.shuffle(shufflesCnt);

        auto startTime = std::chrono::high_resolution_clock::now();
        int cost = search.solve(board);
        auto endTime = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime).count();

        file << board << "," << cost << std::endl;

        infoMessage("Generated solution: shuffles: " + std::to_string(shufflesCnt) + ", cost " + std::to_string(cost) + ", duration: " +
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
