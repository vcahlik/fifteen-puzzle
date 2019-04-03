from prototype.heuristics.pattern_database_heuristic import PatternDatabaseHeuristic
from prototype.experiments.board_solving_experiment import BoardSolvingExperiment
from prototype.graph_search.search_algorithms import AStarSearch
from prototype.experiments.dataset_generator import DatasetGenerator
from prototype.heuristics.ann_heuristic import ANNHeuristic
from prototype.board import ChaoticShufflingBoardsGenerator
import prototype.constants as constants
import os


def create_experiment(output_file_path):
    algorithms = list()
    algorithms.append(AStarSearch())
    # algorithms.append(IDAStarSearch())

    heuristics = list()

    pdb = PatternDatabaseHeuristic(5)
    # pdb.pre_calculate_db()
    pdb.load_db()
    heuristics.append(pdb)

    model_path = os.path.join(constants.PROJECT_ROOT, 'data/keras-1024-1024-512-128-64.h5')
    heuristics.append(ANNHeuristic(model_path, additive_constant=0, label=""))

    boards_generator = ChaoticShufflingBoardsGenerator(100)
    return BoardSolvingExperiment(
        algorithms,
        heuristics,
        boards_generator,
        output_file_path=output_file_path)


def process_entry_point(**kwargs):
    experiment = create_experiment(**kwargs)
    experiment.start()


if __name__ == "__main__":
    # output_file_path = constants.PROJECT_ROOT + "/data/experiments/chaotic-generator-heuristic-benchmark.csv"
    output_file_path = None
    kwargs = {"output_file_path": output_file_path}
    experiment = create_experiment(output_file_path)

    dataset_generator = DatasetGenerator(process_entry_point, kwargs, output_file_path, experiment.print_csv_column_names_row)
    dataset_generator.run()
