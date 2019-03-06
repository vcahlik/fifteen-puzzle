import numpy as np
from .heuristic import Heuristic


class NeuralNetworkHeuristic(Heuristic):
    def __init__(self, model, custom_name=None):
        super().__init__(custom_name)
        self.model = model

    def estimate_cost(self, board):
        x = np.array(board.config)
        x_encoded = np.eye(16)[x].ravel()
        y = self.model.predict(x_encoded.reshape(1, -1)).item()
        return y
