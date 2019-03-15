from prototype.board import Board
from prototype.utils import debug_print
import time
from prototype.graph_search.node import ForwardSearchNode


class SolvingExperiment:
    def __init__(self, algorithms: list, heuristics: list, n_shuffles: int, n_runs: int = -1):
        self.algorithms = algorithms
        self.heuristics = heuristics
        self.n_shuffles = n_shuffles
        self.n_runs = n_runs

        self.run_no = 0
        self.results = []

    def _solve(self, board, algorithm, heuristic):
        start_time = time.clock()
        algorithm.run(ForwardSearchNode(board))
        path, expanded_nodes = iterative_deepening_a_star_search(ForwardSearchNode(board), heuristic)
        cost = len(path) - 1
        end_time = time.clock()
        duration = end_time - start_time

        durations.append(duration)
        mh_mean_duration = np.mean(durations)
        debug_print(f"Experiment: {type(heuristic).__name__}: len: {cost}\t\texpanded: {expanded_nodes}\
                \t\tduration: {round(duration, 6)}\t\tmean duration: {mh_mean_duration}")

        return cost

    def start(self):
        try:
            while True:
                self.run_no = self.run_no + 1

                board = Board()
                board.shuffle(self.n_shuffles)

                for algorithm in self.algorithms:
                    for heuristic in self.heuristics:
                        self._solve(board, algorithm, heuristic)

                if self.run_no >= self.n_runs > 0:
                    break
        except KeyboardInterrupt:
            debug_print("Interrupted by user.")
