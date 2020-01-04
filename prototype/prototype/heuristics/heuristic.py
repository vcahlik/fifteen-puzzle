class Heuristic:
    """
    A heuristic function to estimate optimal solution costs.
    """

    def estimate_cost(self, board):
        """
        Estimate the optimal solution cost of a board.
        """
        pass

    def name(self):
        return self.__class__.__name__

    def set_goal(self, board):
        """
        Sets the target state (usually the goal state).
        """
        raise NotImplementedError()
