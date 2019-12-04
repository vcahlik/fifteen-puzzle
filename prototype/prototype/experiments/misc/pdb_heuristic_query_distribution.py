from prototype.heuristics.cpp_pdb_heuristic import CppPatternDatabaseHeuristic
from prototype.graph_search.search_algorithms import AStarSearch, IDAStarSearch
from prototype.board import RandomBoardsGenerator
from prototype.algorithm import ResultType
import random
import prototype.constants as constants
from prototype.utils import debug_print


ida_star_global = IDAStarSearch()
pdb_global = CppPatternDatabaseHeuristic(8)
pdb_global.load_db()
ida_star_global.heuristic = pdb_global


def callback(board):
    path = constants.PROJECT_ROOT + "/data/experiments/pdb-heuristic-query-distribution.csv"
    with open(path, 'a') as f:
        if random.random() < 0.00001:
            ida_star_global.run(board)
            optimal_solution_cost = ida_star_global.results[ResultType.SOLUTION_COST.name]
            debug_print(str(optimal_solution_cost))
            f.write(str(optimal_solution_cost) + "\n")


if __name__ == "__main__":
    path = constants.PROJECT_ROOT + "/data/experiments/pdb-heuristic-query-distribution.csv"
    with open(path, 'w') as f:
        f.write("OPTIMAL_SOLUTION_COST\n")

    boards_generator = RandomBoardsGenerator(4)
    a_star = AStarSearch()
    pdb = CppPatternDatabaseHeuristic(8, callback=callback)
    pdb.load_db()
    a_star.heuristic = pdb

    while True:
        debug_print("New board.")
        board = boards_generator.random_board()
        a_star.run(board)
