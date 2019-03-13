import numpy as np
from .heuristic import Heuristic


class NeuralNetworkHeuristic(Heuristic):
    def __init__(self, model, additive_constant=0, custom_name=None):
        super().__init__(custom_name)
        self.model = model
        self.additive_constant = additive_constant

    def estimate_cost(self, board):
        x = np.array(board.config)
        x_encoded = np.eye(16)[x].ravel()
        y = self.model.predict(x_encoded.reshape(1, -1)).item()
        return y + float(self.additive_constant)
