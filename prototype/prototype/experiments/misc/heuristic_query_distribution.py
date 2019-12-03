from prototype.heuristics.cpp_pdb_heuristic import CppPatternDatabaseHeuristic
from prototype.graph_search.search_algorithms import AStarSearch, IDAStarSearch
from prototype.board import RandomBoardsGenerator
from prototype.algorithm import ResultType


ida_star_global = IDAStarSearch()
pdb_global = CppPatternDatabaseHeuristic(5)
pdb_global.load_db()
ida_star_global.heuristic = pdb_global


def callback(board):
    ida_star_global.run(board)
    optimal_solution_cost = ida_star_global.results[ResultType.SOLUTION_COST.name]
    print(optimal_solution_cost)


if __name__ == "__main__":
    boards_generator = RandomBoardsGenerator(4)
    a_star = AStarSearch()
    pdb = CppPatternDatabaseHeuristic(5, callback=callback)
    pdb.load_db()
    a_star.heuristic = pdb

    while True:
        board = boards_generator.random_board()
        a_star.run(board)
