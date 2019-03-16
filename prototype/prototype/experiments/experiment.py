from prototype.board import Board
from prototype.utils import debug_print, atomic_row_write
from prototype.graph_search.node import ForwardSearchNode
from prototype.algorithm import Algorithm


class Experiment:
    def __init__(self, algorithms: list, heuristics: list, boards_generator, n_runs: int = -1, output_file_path=None):
        self.algorithms = algorithms
        self.heuristics = heuristics
        self.boards_generator = boards_generator
        self.n_runs = n_runs
        self.output_file_path = output_file_path

        self.board_no = 0
        self.results = []

    def print_csv_column_names_row(self):
        column_names = list()

        column_names.append("BOARD_ID")
        column_names.append("ALGORITHM_NAME")
        column_names.append("HEURISTIC_NAME")

        result_type_names = [result_type for result_type in Algorithm.get_default_results().keys()]
        column_names.extend(result_type_names)

        row = ",".join(column_names)
        print(row)
        if self.output_file_path is not None:
            atomic_row_write(self.output_file_path, row)

    def print_csv_results_row(self, algorithm, heuristic):
        algorithm_results = ["" if value is None else str(round(value, 6)) for value in algorithm.results.values()]

        values = list()

        values.append(str(self.board_no))
        values.append(algorithm.name())
        values.append(heuristic.name())
        values.extend(algorithm_results)

        row = ",".join(values)
        print(row)
        if self.output_file_path is not None:
            atomic_row_write(self.output_file_path, row)

    def _solve(self, board, algorithm, heuristic):
        algorithm.heuristic = heuristic
        algorithm.run(ForwardSearchNode(board))

        self.print_csv_results_row(algorithm, heuristic)

    def start(self):
        try:
            while True:
                self.board_no = self.board_no + 1

                board = self.boards_generator.random_board()

                for algorithm in self.algorithms:
                    for heuristic in self.heuristics:
                        self._solve(board, algorithm, heuristic)

                if self.board_no >= self.n_runs > 0:
                    break
        except KeyboardInterrupt:
            debug_print("Interrupted by user.")
