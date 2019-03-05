from neural.keras_mlp import KerasMLP


class NeuralNetworkHeuristic:
    def __init__(self, **kwargs):
        self.net = KerasMLP(**kwargs)

    def train(self, **kwargs):
        self.net.train(**kwargs)

    def cost(self, board):
        # TODO
        return None
