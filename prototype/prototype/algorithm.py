from prototype.board import Board


class Algorithm:
    def __init__(self, goal_test, metric=None):
        self.goal_test = goal_test
        self.metric = metric
