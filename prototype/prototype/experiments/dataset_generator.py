from prototype.utils import debug_print
import multiprocessing
import pathlib
import os
import datetime


class DatasetGenerator:
    def __init__(self, entry_point, kwargs, dataset_path, column_names_write_function):
        self.entry_point = entry_point
        self.kwargs = kwargs
        self.dataset_path = dataset_path
        self.column_names_write_function = column_names_write_function

    def _ensure_file_has_column_names_row(self):
        if not pathlib.Path(self.dataset_path).exists():
            self.column_names_write_function()

    def run(self, n_processes=-1):
        if n_processes < 1:
            n_processes = multiprocessing.cpu_count()

        self._ensure_file_has_column_names_row()

        processes = []
        for i in range(0, n_processes):
            p = multiprocessing.Process(target=self.entry_point, kwargs=self.kwargs)
            p.start()
            processes.append(p)

        debug_print(f"Dataset generator started with {n_processes} processes.")
