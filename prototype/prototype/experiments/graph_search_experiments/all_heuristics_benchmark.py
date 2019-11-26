from prototype.heuristics.cpp_pdb_heuristic import CppPatternDatabaseHeuristic
from prototype.experiments.board_solving_experiment import BoardSolvingExperiment
from prototype.graph_search.search_algorithms import AStarSearch, IDAStarSearch
from prototype.experiments.dataset_generator import DatasetGenerator
from prototype.heuristics.ann_heuristic import ANNHeuristic
from prototype.board import RandomBoardsGenerator
import prototype.constants as constants
import os


def create_experiment(output_file_path):
    algorithms = list()
    # algorithms.append(AStarSearch())
    algorithms.append(IDAStarSearch())

    heuristics = list()

    # pdb = CppPatternDatabaseHeuristic(8)
    # pdb.load_db()
    # heuristics.append(pdb)

    # model_path = os.path.join(constants.PROJECT_ROOT, 'data/neural-networks/keras-1024-1024-512-128-64.h5')
    # heuristics.append(ANNHeuristic(model_path, label="MSE"))

    model_path = os.path.join(constants.PROJECT_ROOT, 'data/neural-networks/keras-1024-512-256-128-64-mse.h5')
    heuristics.append(ANNHeuristic(model_path, label="MSE"))

    # model_path = os.path.join(constants.PROJECT_ROOT, 'data/neural-networks/keras-1024-512-256-128-64-amse02.h5')
    # heuristics.append(ANNHeuristic(model_path, label="AMSE0.2"))
    #
    # model_path = os.path.join(constants.PROJECT_ROOT, 'data/neural-networks/keras-1024-512-256-128-64-amse04.h5')
    # heuristics.append(ANNHeuristic(model_path, label="AMSE0.4"))
    #
    # model_path = os.path.join(constants.PROJECT_ROOT, 'data/neural-networks/keras-1024-512-256-128-64-amse06.h5')
    # heuristics.append(ANNHeuristic(model_path, label="AMSE0.6"))

    boards_generator = RandomBoardsGenerator(4)
    return BoardSolvingExperiment(
        algorithms,
        heuristics,
        boards_generator,
        output_file_path=output_file_path)


def process_entry_point(**kwargs):
    experiment = create_experiment(**kwargs)
    experiment.start()


if __name__ == "__main__":
    output_file_path = constants.PROJECT_ROOT + "/data/experiments/all-heuristics-benchmark.csv"
    kwargs = {"output_file_path": output_file_path}
    experiment = create_experiment(output_file_path)

    dataset_generator = DatasetGenerator(process_entry_point, kwargs, output_file_path, experiment.print_csv_column_names_row)
    dataset_generator.run(n_processes=1)
