from prototype.heuristics.cpp_pdb_heuristic import CppPatternDatabaseHeuristic
from prototype.graph_search.search_algorithms import AStarSearch, IDAStarSearch
from prototype.board import RandomBoardsGenerator
from prototype.algorithm import ResultType
from prototype.heuristics.ann_heuristic import ANNHeuristic
from tensorflow.keras import backend as K
import random
import prototype.constants as constants
from prototype.utils import debug_print
import os


ida_star_global = IDAStarSearch()
pdb_global = CppPatternDatabaseHeuristic(8)
pdb_global.load_db()
ida_star_global.heuristic = pdb_global


def callback(board):
    path = constants.PROJECT_ROOT + "/data/experiments/ann-heuristic-keras-1024-1024-512-128-64-v3-query-distribution.csv"
    with open(path, 'a') as f:
        if random.random() < 0.001:
            ida_star_global.run(board)
            optimal_solution_cost = ida_star_global.results[ResultType.SOLUTION_COST.name]
            debug_print(str(optimal_solution_cost))
            f.write(str(optimal_solution_cost) + "\n")


if __name__ == "__main__":
    path = constants.PROJECT_ROOT + "/data/experiments/ann-heuristic-keras-1024-1024-512-128-64-v3-query-distribution.csv"
    with open(path, 'w') as f:
        f.write("OPTIMAL_SOLUTION_COST\n")

    boards_generator = RandomBoardsGenerator(4)
    a_star = AStarSearch()

    model_path = os.path.join(constants.PROJECT_ROOT, 'data/neural-networks/v3/keras-1024-1024-512-128-64-v3.h5')
    annh = ANNHeuristic(model_path, "MSE", callback=callback)

    a_star.heuristic = annh

    while True:
        debug_print("New board.")
        board = boards_generator.random_board()
        a_star.run(board)
