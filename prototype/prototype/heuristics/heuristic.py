class Heuristic:
    def estimate_cost(self, board):
        pass

    def name(self):
        return self.__class__.__name__

    def set_goal(self, board):
        raise NotImplementedError()
