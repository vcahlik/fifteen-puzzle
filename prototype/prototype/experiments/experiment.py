from prototype.board import Board
from prototype.utils import debug_print, atomic_row_write, timestamped_process_id
from prototype.graph_search.node import ForwardSearchNode
from prototype.algorithm import Algorithm


class Experiment:
    def __init__(self,
                 n_runs: int = -1,
                 output_file_path=None):
        self.n_runs = n_runs
        self.output_file_path = output_file_path

        self.process_id = timestamped_process_id()
