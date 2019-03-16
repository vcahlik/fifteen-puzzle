import multiprocessing
import pathlib


class DatasetGenerator:
    def __init__(self, entry_point, args, dataset_path, column_names_write_function):
        self.entry_point = entry_point
        self.args = args
        self.dataset_path = dataset_path
        self.column_names_write_function = column_names_write_function

    def run(self, n_processes=6):
        if not pathlib.Path(self.dataset_path).exists():
            self.column_names_write_function()

        processes = []
        for i in range(0, 6):
            p = multiprocessing.Process(target=self.entry_point, args=self.args)
            p.start()
            processes.append(p)

