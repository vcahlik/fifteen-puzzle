#include <iostream>
#include "Board.h"
#include <chrono>

void randomBoardsBenchmark() {
    auto startTime = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < 10000; ++i) {
        Board board;
        board.shuffle(500);
    }

    auto endTime = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime).count();

    std::cout << duration << " seconds" << std::endl;
}

int main(int argc, char **argv) {
    randomBoardsBenchmark();
}