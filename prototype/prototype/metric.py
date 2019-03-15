from enum import Enum


class MetricType(Enum):
    N_EXPANDED_NODES = 1
    SOLUTION_COST = 2
    REAL_TIME = 3


class Metric:
    def __init__(self, type: str):
        self.type = type

    def reset(self):
        pass

    def add_record(self, record):
        pass

    def score(self):
        pass
