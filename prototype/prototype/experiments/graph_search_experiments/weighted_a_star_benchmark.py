from prototype.heuristics.cpp_pdb_heuristic import CppPatternDatabaseHeuristic
from prototype.experiments.board_solving_experiment import BoardSolvingExperiment
from prototype.graph_search.search_algorithms import AStarSearch, IDAStarSearch
from prototype.experiments.dataset_generator import DatasetGenerator
from prototype.heuristics.ann_heuristic import ANNHeuristic
from prototype.board import RandomBoardsGenerator, ShufflingBoardsGenerator
from tensorflow.keras import backend as K
import prototype.constants as constants
import os
import keras


def create_experiment(output_file_path):
    algorithms = list()
    # algorithms.append(AStarSearch())
    algorithms.append(AStarSearch())

    heuristics = list()

    ############################################
    # An admissible heuristic should be first! #
    ############################################

    pdb = CppPatternDatabaseHeuristic(8, weight=1.15)
    pdb.load_db()
    heuristics.append(pdb)

    pdb2 = CppPatternDatabaseHeuristic(8, weight=1.20)
    pdb2.load_db()
    heuristics.append(pdb2)

    pdb3 = CppPatternDatabaseHeuristic(8, weight=1.25)
    pdb3.load_db()
    heuristics.append(pdb3)

    boards_generator = RandomBoardsGenerator(4)
    return BoardSolvingExperiment(
        algorithms,
        heuristics,
        boards_generator,
        output_file_path=output_file_path,
        include_optimal_solver=False)


def process_entry_point(**kwargs):
    experiment = create_experiment(**kwargs)
    experiment.start()


if __name__ == "__main__":
    output_file_path = constants.PROJECT_ROOT + "/data/experiments/weighted-a-star-benchmark.csv"
    kwargs = {"output_file_path": output_file_path}

    dataset_generator = DatasetGenerator(process_entry_point, kwargs, output_file_path, None)
    dataset_generator.run(n_processes=1)
