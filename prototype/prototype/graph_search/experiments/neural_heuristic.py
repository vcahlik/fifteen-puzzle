from board import Board
from graph_search.node import ForwardSearchNode
from graph_search.algorithms.iterative_deepening_a_star_search import iterative_deepening_a_star_search
from graph_search.heuristics.manhattan_distance import ManhattanDistanceHeuristic
from graph_search.heuristics.neural_network import NeuralNetworkHeuristic
from graph_search.heuristics.pattern_database import PatternDatabaseHeuristic
from utils import debug_print
import time
import numpy as np
import keras


def solve(board, heuristic, durations):
    start_time = time.clock()
    path, expanded_nodes = iterative_deepening_a_star_search(ForwardSearchNode(board), heuristic)
    cost = len(path) - 1
    end_time = time.clock()
    duration = end_time - start_time

    durations.append(duration)
    mh_mean_duration = np.mean(durations)
    debug_print(f"Experiment: {type(heuristic).__name__}: len: {cost}\t\texpanded: {expanded_nodes}\
            \t\tduration: {round(duration, 6)}\t\tmean duration: {mh_mean_duration}")

    return cost


def experiment(n_shuffles, heuristics, n_runs=-1):
    durations = {heuristic: list() for heuristic in heuristics}
    i = 0

    while True:
        i = i + 1

        board = Board()
        board.shuffle(n_shuffles)

        solution_lengths = set()

        for heuristic in heuristics:
            current_heuristic_durations = durations[heuristic]
            cost = solve(board, heuristic, current_heuristic_durations)
            solution_lengths.add(cost)

        if len(solution_lengths) > 1:
            debug_print("Optimal solution lengths mismatch!")

        if i >= n_runs > 0:
            return


heuristics = list()

pdb = PatternDatabaseHeuristic(4)
# pdb.pre_calculate_db()
pdb.load_db()
heuristics.append(pdb)

# model = keras.models.load_model('../../../../data/keras-1024-1024-512-128-64.h5')
# heuristics.append(NeuralNetworkHeuristic(model, custom_name="Neural"))

# model = keras.models.load_model('../../../../data/keras-1024-1024-512-128-64.h5')
# heuristics.append(NeuralNetworkHeuristic(model, additive_constant=-2, custom_name="Neural, shift -2"))

experiment(80, heuristics)
