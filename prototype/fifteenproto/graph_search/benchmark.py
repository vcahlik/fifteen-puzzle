from board import Board
from graph_search.algorithms.a_star_search import a_star_search
from graph_search.algorithms.iterative_deepening_a_star_search import iterative_deepening_a_star_search
from graph_search.node import ForwardSearchNode
from utils import debug_print
import time
import numpy as np


def benchmark(n_shuffles, heuristics, n_runs=-1):
    durations = {heuristic: list() for heuristic in heuristics}
    i = 0

    while True:
        i = i + 1

        board = Board()
        board.shuffle(n_shuffles)

        solution_lengths = set()

        for heuristic in heuristics:
            current_heuristic_durations = durations[heuristic]
            start_time = time.clock()
            path, expanded_nodes = a_star_search(ForwardSearchNode(board), heuristic)
            cost = len(path) - 1
            end_time = time.clock()

            duration = end_time - start_time
            current_heuristic_durations.append(duration)
            last_n_mean_duration = np.mean(current_heuristic_durations[-100:])
            debug_print(f"Benchmark: {type(heuristic).__name__}: len: {cost}\t\texpanded: {expanded_nodes}\
                    \t\tduration: {round(duration, 6)}\t\tmean duration of last n: {last_n_mean_duration}")

            if heuristic.cost(board) > cost:
                print(board)

                raise RuntimeError(f"Heuristic not admissible! (estimated: {heuristic.cost(board)}, real: {cost})")

            solution_lengths.add(cost)
            if len(solution_lengths) > 1:
                raise RuntimeError("Optimal solution lengths mismatch!")

        if i >= n_runs > 0:
            return


def check_heuristics_equality(heuristics):
    while True:
        board = Board()
        board.shuffle(1000)

        heuristic_estimates = set()

        for heuristic in heuristics:
            heuristic_estimates.add(heuristic.cost(board))
            if len(heuristic_estimates) > 1:
                raise RuntimeError("Heuristics are not equal.")

        print("equal")
