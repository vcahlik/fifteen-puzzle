from prototype.heuristics.cpp_pdb_heuristic import CppPatternDatabaseHeuristic
from prototype.graph_search.search_algorithms import AStarSearch, IDAStarSearch
from prototype.board import RandomBoardsGenerator
from prototype.algorithm import ResultType
from prototype.heuristics.ann_heuristic import ANNHeuristic
import prototype.constants as constants
import os


h = CppPatternDatabaseHeuristic(8)
h.load_db()
ida_star = IDAStarSearch(h)
boards_generator = RandomBoardsGenerator(4)

model_path = os.path.join(constants.PROJECT_ROOT, 'data/neural-networks/keras-1024-1024-512-128-64.h5')
annh1 = ANNHeuristic(model_path, label="MSE")

model_path = os.path.join(constants.PROJECT_ROOT, 'data/neural-networks/keras-1024-512-256-128-64-mse.h5')
annh2 = ANNHeuristic(model_path, label="MSE")

with open('results.csv', 'w') as f:
    f.write(f"real_cost,keras-1024-1024-512-128-64.h5,keras-1024-512-256-128-64-mse.h5\n")
    while True:
        board = boards_generator.random_board()
        ida_star.heuristic = h
        ida_star.run(board)
        cost = ida_star.results[ResultType.SOLUTION_COST.name]
        h1cost = annh1.estimate_cost(board)
        h2cost = annh2.estimate_cost(board)
        f.write(f"{cost},{h1cost},{h2cost}\n")
        print(f"{cost},{h1cost},{h2cost}")
