#include <iostream>
#include "Board.h"
#include <chrono>
#include <StateSpaceSearch/Heuristics/ManhattanDistance.h>
#include <StateSpaceSearch/Algorithms/IDAStar.h>
#include <array>

void randomBoardsBenchmark() {
    auto startTime = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < 10000; ++i) {
        Board board;
        board.shuffle(500);
    }

    auto endTime = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime).count();

    std::cout << duration << " milliseconds" << std::endl;
}

void randomSolveBenchmark() {
    auto startTime = std::chrono::high_resolution_clock::now();

    ManhattanDistance heuristic;
    IDAStar search(heuristic);

    for (int i = 0; i < 200; ++i) {
        Board board;
        board.shuffle(500);
        std::cout << search.solve(board) << std::endl;
    }

    auto endTime = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime).count();

    std::cout << duration << " milliseconds" << std::endl;
}

int main(int argc, char **argv) {
//    randomBoardsBenchmark();
    randomSolveBenchmark();

//    ManhattanDistance heuristic;
//    IDAStar search(heuristic);
//
//    std::array<int, 16> pebbles = {5, 11, 6, 13, 14, 8, 7, 0, 15, 2, 4, 1, 10, 3, 9, 12};
//    Board board = Board(pebbles);
//
//    auto startTime = std::chrono::high_resolution_clock::now();
//
//    std::cout << search.solve(board) << std::endl;
//
//    auto endTime = std::chrono::high_resolution_clock::now();
//    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime).count();
//
//    std::cout << duration << " milliseconds" << std::endl;
}