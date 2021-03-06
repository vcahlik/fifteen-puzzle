from enum import Enum


class ResultType(Enum):
    RUN_TIME = 1
    SOLUTION_COST = 2
    EXPANDED_NODES = 3
    INITIAL_HEURISTIC_PREDICTION = 4


class Algorithm:
    """
    A base class for an algorithm solving the (N^2-1)-puzzle.
    """

    def __init__(self, goal_test):
        self.goal_test = goal_test
        self.results = dict()

    @staticmethod
    def get_default_results():
        return {
            ResultType.RUN_TIME.name: None,
            ResultType.SOLUTION_COST.name: None,
            ResultType.EXPANDED_NODES.name: None,
            ResultType.INITIAL_HEURISTIC_PREDICTION.name: None
        }

    def name(self):
        return self.__class__.__name__

    def get_result(self, result_type: ResultType):
        """
        Returns a single result.
        """
        try:
            return self.results[result_type]
        except KeyError:
            return None

    def reset_results(self):
        """
        Resets the stored results to their defaults.
        """
        self.results = Algorithm.get_default_results()
