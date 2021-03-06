from prototype.board import Board
from prototype.utils import debug_print, atomic_row_write, timestamped_process_id
from prototype.graph_search.node import ForwardSearchNode
from prototype.algorithm import Algorithm
from prototype.experiments.experiment import Experiment
from prototype.graph_search.search_algorithms import IDAStarSearch


class BoardSolvingExperiment(Experiment):
    """
    An experiment in which random boards solved with different algorithms and heuristics.
    """

    def __init__(self,
                 algorithms: list,
                 heuristics: list,
                 boards_generator,
                 n_runs: int = -1,
                 output_file_path=None,
                 include_optimal_solver=False):
        super().__init__(n_runs, output_file_path)
        self.algorithms = algorithms
        self.heuristics = heuristics
        self.boards_generator = boards_generator
        self.include_optimal_solver = include_optimal_solver

        self.board_no = 0

    def print_csv_column_names_row(self):
        """
        Prints the header row of the CSV.
        """
        column_names = list()

        column_names.append("PROCESS_ID")
        column_names.append("BOARD_ID")
        column_names.append("ALGORITHM_NAME")
        column_names.append("HEURISTIC_NAME")
        column_names.append("BOARDS_GENERATOR_NAME")

        result_type_names = [result_type for result_type in Algorithm.get_default_results().keys()]
        column_names.extend(result_type_names)

        row = ",".join(column_names)
        print(row)
        if self.output_file_path is not None:
            atomic_row_write(self.output_file_path, row)

    def print_csv_results_row(self, algorithm, heuristic):
        """
        Prints a single CSV row with results.
        """
        algorithm_results = ["" if value is None else str(round(value, 6)) for value in algorithm.results.values()]

        values = list()

        values.append(str(self.process_id))
        values.append(str(self.board_no))
        values.append(algorithm.name())
        values.append(heuristic.name())
        values.append(self.boards_generator.name())
        values.extend(algorithm_results)

        row = ",".join(values)
        print(row)
        if self.output_file_path is not None:
            atomic_row_write(self.output_file_path, row)

    def _solve(self, board, algorithm, heuristic):
        """
        Runs the specified algorithm with specified heuristic on the speficied board an prints the results to a CSV.
        """
        algorithm.heuristic = heuristic
        algorithm.run(board)

        self.print_csv_results_row(algorithm, heuristic)

    def start(self):
        """
        Starts the experiment.
        """
        try:
            ida_star = IDAStarSearch()
            admissible_h = self.heuristics[0]  # The first heuristic should be admissible!
            while True:
                self.board_no = self.board_no + 1

                board = self.boards_generator.random_board()

                if self.include_optimal_solver:
                    self._solve(board, ida_star, admissible_h)

                for algorithm in self.algorithms:
                    for heuristic in self.heuristics:
                        self._solve(board, algorithm, heuristic)

                if self.board_no >= self.n_runs > 0:
                    break
        except KeyboardInterrupt:
            debug_print("Interrupted by user.")
