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

    pdb = CppPatternDatabaseHeuristic(8)
    pdb.load_db()
    heuristics.append(pdb)

    pdb2 = CppPatternDatabaseHeuristic(8, weight=1.1)
    pdb2.load_db()
    heuristics.append(pdb2)

    pdb3 = CppPatternDatabaseHeuristic(8, weight=1.2)
    pdb3.load_db()
    heuristics.append(pdb3)

    pdb4 = CppPatternDatabaseHeuristic(8, weight=1.3)
    pdb4.load_db()
    heuristics.append(pdb4)

    model_path = os.path.join(constants.PROJECT_ROOT, 'data/neural-networks/v3/keras-1024-1024-512-128-64-v3.h5')
    heuristics.append(ANNHeuristic(model_path, label="MSE"))

    model_path = os.path.join(constants.PROJECT_ROOT, 'data/neural-networks/v3/keras-2752-v3.h5')
    heuristics.append(ANNHeuristic(model_path, label="MSE1layer"))

    def asymmetric_mean_squared_error_04(y_true, y_pred):
        return K.mean(K.square(y_pred - y_true) * K.square(K.sign(y_pred - y_true) + 0.4), axis=-1)

    model_path = os.path.join(constants.PROJECT_ROOT, 'data/neural-networks/v3/keras-1024-1024-512-128-64-v3-amse04.h5')
    heuristics.append(ANNHeuristic(model_path, "AMSE0.4", asymmetric_mean_squared_error_04))

    boards_generator = RandomBoardsGenerator(4)
    return BoardSolvingExperiment(
        algorithms,
        heuristics,
        boards_generator,
        output_file_path=output_file_path,
        include_optimal_solver=True)


def process_entry_point(**kwargs):
    experiment = create_experiment(**kwargs)
    experiment.start()


if __name__ == "__main__":
    output_file_path = constants.PROJECT_ROOT + "/data/experiments/all-heuristics-benchmark-v3.csv"
    kwargs = {"output_file_path": output_file_path}

    dataset_generator = DatasetGenerator(process_entry_point, kwargs, output_file_path, None)
    dataset_generator.run(n_processes=1)
