from prototype.board import Board
from prototype.utils import debug_print
from prototype.graph_search.node import ForwardSearchNode
from algorithm import Algorithm
import time


class SolvingExperiment:
    def __init__(self, algorithms: list, heuristics: list, n_shuffles: int, n_runs: int = -1):
        self.algorithms = algorithms
        self.heuristics = heuristics
        self.n_shuffles = n_shuffles
        self.n_runs = n_runs

        self.run_no = 0
        self.results = []

    def print_csv_column_names_row(self):
        column_names = list()

        column_names.append("ALGORITHM_NAME")
        column_names.append("HEURISTIC_NAME")
        column_names.extend(Algorithm.get_default_results().keys())

        print(",".join(column_names))

    def print_csv_results_row(self, algorithm, heuristic):
        values = list()

        values.append(algorithm.name())
        values.append(heuristic.name())
        values.extend(algorithm.results.values())

        print(",".join(values))

    def _solve(self, board, algorithm, heuristic):
        algorithm.heuristic = heuristic
        algorithm.run(ForwardSearchNode(board))

        self.print_csv_results_row(algorithm, heuristic)

        # debug_print(f"Experiment: {type(heuristic).__name__}: len: {cost}\t\texpanded: {expanded_nodes}\
        #         \t\tduration: {round(duration, 6)}\t\tmean duration: {mh_mean_duration}")

    def start(self):
        try:
            while True:
                self.run_no = self.run_no + 1

                board = Board()
                board.shuffle(self.n_shuffles)

                self.print_csv_column_names_row()

                for algorithm in self.algorithms:
                    for heuristic in self.heuristics:
                        self._solve(board, algorithm, heuristic)

                if self.run_no >= self.n_runs > 0:
                    break
        except KeyboardInterrupt:
            debug_print("Interrupted by user.")
