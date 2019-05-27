from prototype.heuristics.cpp_pdb_heuristic import CppPatternDatabaseHeuristic
from prototype.experiments.board_solving_experiment import BoardSolvingExperiment
from prototype.graph_search.search_algorithms import AStarSearch
from prototype.experiments.dataset_generator import DatasetGenerator
from prototype.heuristics.ann_heuristic import ANNHeuristic
from prototype.board import RandomBoardsGenerator
import prototype.constants as constants
import os


def create_experiment(output_file_path):
    algorithms = list()
    algorithms.append(AStarSearch())
    # algorithms.append(IDAStarSearch())

    heuristics = list()

    pdb1 = CppPatternDatabaseHeuristic(8)
    pdb1.load_db()
    heuristics.append(pdb1)

    model1_path = os.path.join(constants.PROJECT_ROOT, 'data/keras-1024-1024-512-128-64.h5')
    heuristics.append(ANNHeuristic(model1_path, label="small"))

    # model2_path = os.path.join(constants.PROJECT_ROOT, 'data/keras-large-4096-4096-4096-2048-2048-2048-1024-1024-1024_2019-03-26 00:08:21.060033.h5')
    # heuristics.append(ANNHeuristic(model2_path, label="large"))

    boards_generator = RandomBoardsGenerator()
    return BoardSolvingExperiment(
        algorithms,
        heuristics,
        boards_generator,
        output_file_path=output_file_path)


def process_entry_point(**kwargs):
    experiment = create_experiment(**kwargs)
    experiment.start()


if __name__ == "__main__":
    # output_file_path = constants.PROJECT_ROOT + "/data/experiments/ann-heuristic-benchmark-pdb8.csv"
    output_file_path = None
    kwargs = {"output_file_path": output_file_path}
    experiment = create_experiment(output_file_path)

    dataset_generator = DatasetGenerator(process_entry_point, kwargs, output_file_path, experiment.print_csv_column_names_row)
    dataset_generator.run(n_processes=2)
