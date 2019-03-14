import keras
import numpy as np


class KerasMLP:
    def __init__(self, **kwargs):
        self.model = self.create_model(**kwargs)

    def cost(self, board):
        x = np.array(board.config)
        x_encoded = np.eye(16)[x].ravel()
        y = self.model.predict(x_encoded.reshape(1, -1)).item()
        return y

    @staticmethod
    def create_model(
            layer_sizes,
            learning_rate=0.001,
            dropout_ratio=0.2,
            activation='elu',
            kernel_initializer='he_normal',
            batch_normalize=True):

        model = keras.models.Sequential()
        model.add(keras.layers.Dense(layer_sizes[0],
                                     input_shape=(256,),
                                     activation=activation,
                                     kernel_initializer=kernel_initializer))
        model.add(keras.layers.Activation(activation))
        if batch_normalize:
            model.add(keras.layers.normalization.BatchNormalization())
        model.add(keras.layers.Dropout(dropout_ratio))

        for layer_size in layer_sizes[1:]:
            model.add(keras.layers.Dense(layer_size, activation=activation, kernel_initializer=kernel_initializer))
            model.add(keras.layers.Activation(activation))
            if batch_normalize:
                model.add(keras.layers.normalization.BatchNormalization())
            model.add(keras.layers.Dropout(dropout_ratio))

        model.add(keras.layers.Dense(1, kernel_initializer=kernel_initializer))
        model.compile(loss='mean_squared_error',
                      optimizer=keras.optimizers.Adam(lr=learning_rate))
        return model
