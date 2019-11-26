import numpy as np
from prototype.heuristics.heuristic import Heuristic


class ANNHeuristic(Heuristic):
    def __init__(self, model_path, label=None):
        self.model_path = model_path
        self.label = label

        self._model = None

    def get_model(self):
        import tensorflow.keras  # Must be loaded in the worker process!

        if self._model is None:
            self._model = tensorflow.keras.models.load_model(self.model_path)

        return self._model

    def estimate_cost(self, board):
        x = np.array(board.config)
        x_encoded = np.eye(board.N**2)[x].ravel()
        y = self.get_model().predict(x_encoded.reshape(1, -1)).item()
        return y

    def name(self):
        if self.label is not None:
            return f"ANN[Label:{self.label}]"
        else:
            return f"ANN"
