class Algorithm:
    def __init__(self, goal_test, metrics: list = None):
        if metrics is None:
            metrics = list()

        self.goal_test = goal_test
        self.metrics = metrics
