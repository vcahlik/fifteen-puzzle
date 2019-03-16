import numpy as np
from prototype.heuristics.heuristic import Heuristic


class ANNHeuristic(Heuristic):
    def __init__(self, model, additive_constant=0, custom_name=None):
        super().__init__(custom_name)
        self.model = model
        self.additive_constant = additive_constant

    def estimate_cost(self, board):
        x = np.array(board.config)
        x_encoded = np.eye(16)[x].ravel()
        y = self.model.predict(x_encoded.reshape(1, -1)).item()
        return y + float(self.additive_constant)

    def name(self):
        if self.custom_name is not None:
            return self.custom_name

        name = self.__class__.__name__ + f"[Additive constant: {self.additive_constant}]"
        return name
