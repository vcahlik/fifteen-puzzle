class Heuristic:
    def __init__(self, metrics: list = None, custom_name: str = None):
        if metrics is None:
            metrics = list()

        self.metrics = metrics
        self.custom_name = custom_name

    def estimate_cost(self, board):
        pass

    def name(self):
        if self.custom_name is not None:
            return self.custom_name

        return self.__class__.__name__
