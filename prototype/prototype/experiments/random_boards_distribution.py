from prototype.heuristics.pattern_database_heuristic import PatternDatabaseHeuristic
from prototype.experiments.experiment import Experiment
from prototype.board import RandomBoardsGenerator
from prototype.graph_search.search_algorithms import AStarSearch
from prototype.experiments.dataset_generator import DatasetGenerator
import prototype.constants as constants


def create_experiment(output_file_path):
    algorithms = list()
    algorithms.append(AStarSearch())

    heuristics = list()

    pdb = PatternDatabaseHeuristic(5)
    # pdb.pre_calculate_db()
    pdb.load_db()
    heuristics.append(pdb)

    boards_generator = RandomBoardsGenerator()
    return Experiment(algorithms, heuristics, boards_generator, output_file_path=output_file_path)


def process_entry_point(output_file_path):
    experiment = create_experiment(output_file_path)
    experiment.start()


if __name__ == "__main__":
    output_file_path = constants.PROJECT_ROOT + "/data/experiments/random_boards.csv"
    args = (output_file_path,)
    experiment = create_experiment(output_file_path)

    dataset_generator = DatasetGenerator(process_entry_point, args, output_file_path, experiment.print_csv_column_names_row)
    dataset_generator.run(4)
