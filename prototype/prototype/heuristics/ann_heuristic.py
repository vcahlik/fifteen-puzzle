import numpy as np
from prototype.heuristics.heuristic import Heuristic


class ANNHeuristic(Heuristic):
    def __init__(self, model_path, additive_constant=0, label=None):
        self.model_path = model_path
        self.additive_constant = additive_constant
        self.label = label

        self._model = None

    def get_model(self):
        import keras  # Must be loaded in the worker process!

        if self._model is None:
            self._model = keras.models.load_model(self.model_path)

        return self._model

    def estimate_cost(self, board):
        x = np.array(board.config)
        x_encoded = np.eye(16)[x].ravel()
        y = self.get_model().predict(x_encoded.reshape(1, -1)).item()
        return y + float(self.additive_constant)

    def name(self):
        if self.label is not None:
            return f"ANN[Const:{self.additive_constant};Label:{self.label}]"
        else:
            return f"ANN[Const:{self.additive_constant}]"
