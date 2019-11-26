import numpy as np
import pickle
from prototype.heuristics.heuristic import Heuristic


class RandomForestHeuristic(Heuristic):
    def __init__(self, model_path, label=None):
        self.model_path = model_path
        self.label = label

        self._model = None

    def get_model(self):
        if self._model is None:
            with open(self.model_path, 'rb') as f:
                self._model = pickle.load(f)

        return self._model

    def estimate_cost(self, board):
        x = np.array(board.config)
        x_encoded = np.eye(board.N)[x].ravel()
        y = self.get_model().predict(x_encoded.reshape(1, -1)).item()
        return y

    def name(self):
        if self.label is not None:
            return f"RF[Label:{self.label}]"
        else:
            return f"RF"
