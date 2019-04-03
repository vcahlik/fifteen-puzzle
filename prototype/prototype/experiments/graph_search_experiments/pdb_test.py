from prototype.heuristics.pattern_database_heuristic import PatternDatabaseHeuristic
from prototype.heuristics.cpp_pdb_heuristic import CppPatternDatabaseHeuristic
from prototype.experiments.board_solving_experiment import BoardSolvingExperiment
from prototype.graph_search.search_algorithms import AStarSearch
from prototype.experiments.dataset_generator import DatasetGenerator
from prototype.heuristics.ann_heuristic import ANNHeuristic
from prototype.board import RandomBoardsGenerator, ShufflingBoardsGenerator
import prototype.constants as constants
import os
from prototype.board import Board


def create_experiment(output_file_path):
    algorithms = list()
    algorithms.append(AStarSearch())

    heuristics = list()

    pdb = PatternDatabaseHeuristic(5)
    pdb.load_db()
    heuristics.append(pdb)

    pdb2 = CppPatternDatabaseHeuristic(8)
    pdb2.load_db()
    heuristics.append(pdb2)

    boards_generator = ShufflingBoardsGenerator(100)
    return BoardSolvingExperiment(
        algorithms,
        heuristics,
        boards_generator,
        output_file_path=output_file_path)


def process_entry_point(**kwargs):
    experiment = create_experiment(**kwargs)
    experiment.start()


if __name__ == "__main__":
    output_file_path = None
    kwargs = {"output_file_path": output_file_path}
    experiment = create_experiment(output_file_path)

    dataset_generator = DatasetGenerator(process_entry_point, kwargs, output_file_path, experiment.print_csv_column_names_row)
    dataset_generator.run(n_processes=1)
