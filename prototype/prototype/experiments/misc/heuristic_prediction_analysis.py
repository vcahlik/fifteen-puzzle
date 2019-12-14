from prototype.heuristics.cpp_pdb_heuristic import CppPatternDatabaseHeuristic
from prototype.graph_search.search_algorithms import AStarSearch, IDAStarSearch
from prototype.board import RandomBoardsGenerator, ChaoticShufflingBoardsGenerator
from prototype.algorithm import ResultType
from prototype.heuristics.ann_heuristic import ANNHeuristic
from tensorflow.keras import backend as K
import random
import prototype.constants as constants
from prototype.utils import debug_print
import os


if __name__ == "__main__":
    path = constants.PROJECT_ROOT + "/data/experiments/heuristic-prediction-analysis.csv"
    with open(path, 'w') as f:
        f.write("PREDICTED,OPTIMAL_SOLUTION_COST\n")

    boards_generator = ChaoticShufflingBoardsGenerator(4, 100)

    ida_star = IDAStarSearch()
    pdb = CppPatternDatabaseHeuristic(8)
    pdb.load_db()
    ida_star.heuristic = pdb

    def asymmetric_mean_squared_error_095(y_true, y_pred):
        return K.mean(K.square(y_pred - y_true) * K.square(K.sign(y_pred - y_true) + 0.95), axis=-1)

    model_path = os.path.join(constants.PROJECT_ROOT, 'data/neural-networks/v3/keras-1024-1024-512-128-64-v3-amse095-1.h5')
    annh = ANNHeuristic(model_path, "AMSE0.95A", asymmetric_mean_squared_error_095)

    while True:
        board = boards_generator.random_board()

        predicted = annh.estimate_cost(board)
        ida_star.run(board)
        optimal_solution_cost = ida_star.results[ResultType.SOLUTION_COST.name]

        debug_print(f"{predicted},{optimal_solution_cost}\n")
        with open(path, 'a') as f:
            f.write(f"{predicted},{optimal_solution_cost}\n")
