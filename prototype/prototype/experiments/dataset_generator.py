from prototype.utils import debug_print
import multiprocessing
import pathlib
import os
import datetime


class DatasetGenerator:
    """
    Generates a dataset CSV file using multiple processes.
    """

    def __init__(self, entry_point, kwargs, dataset_path, column_names_write_function=None):
        self.entry_point = entry_point
        self.kwargs = kwargs
        self.dataset_path = dataset_path
        self.column_names_write_function = column_names_write_function

    def _ensure_file_has_column_names_row(self):
        if self.dataset_path is None:
            return

        if not pathlib.Path(self.dataset_path).exists():
            if self.column_names_write_function is not None:
                self.column_names_write_function()

    def run(self, n_processes=-1):
        """
        Runs the experiment from the specified entry_point with multiple processes.
        """
        if n_processes < 1:
            n_processes = multiprocessing.cpu_count()

        self._ensure_file_has_column_names_row()

        processes = []
        for i in range(0, n_processes):
            p = multiprocessing.Process(target=self.entry_point, kwargs=self.kwargs)
            p.start()
            processes.append(p)

        debug_print(f"Dataset generator started with {n_processes} processes.")
