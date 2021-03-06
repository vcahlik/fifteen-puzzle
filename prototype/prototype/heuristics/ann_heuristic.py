import numpy as np
from prototype.heuristics.heuristic import Heuristic


class ANNHeuristic(Heuristic):
    """
    A heuristic function based on an artificial neural network model.
    """

    def __init__(self, model_path, label=None, custom_loss=None, callback=None):
        self.model_path = model_path
        self.label = label
        self.custom_loss = custom_loss
        self.callback = callback

        self._model = None

    def get_model(self):
        """
        Loads the saved ANN from disk.
        """

        import tensorflow.keras  # Must be loaded in the worker process!

        if self._model is None:
            if self.custom_loss is not None:
                self._model = tensorflow.keras.models.load_model(self.model_path,
                                                                 custom_objects={self.custom_loss.__name__: self.custom_loss})
            else:
                self._model = tensorflow.keras.models.load_model(self.model_path)

        return self._model

    def estimate_cost(self, board):
        """
        Estimate the optimal solution cost of a board.
        """
        if self.callback is not None:
            self.callback(board)

        x = np.array(board.config)
        x_encoded = np.eye(board.N**2)[x].ravel()
        prediction = self.get_model().predict(x_encoded.reshape(1, -1)).item()
        return max(prediction, 0)

    def name(self):
        if self.label is not None:
            return f"ANN[Label:{self.label}]"
        else:
            return f"ANN"
