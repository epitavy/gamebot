import numpy as np


class MLP():
    """A class implementing a multi layer perceptron.

    This class only gives an API for the MLP as a big function, the training being done by
    a genetic algorithm.
    Its intent is to be plugged in the `state_score` function of a minimax class. As a
    consequence, it is a regression network with one neuron in the output layer.
    """

    def __init__(self, shape):
        """Initialize the MLP with the given shape.

        The shape is an array of integers giving the number of neurons by layer.
        """
        if len(shape) < 2 or shape[-1] != 1:
            return ValueError("Bad shape for MLP")

        self.shape = shape
        self.layers = []
        for i in range(len(shape) - 1):
            weights = np.random.uniform(-1, 1, (shape[i + 1], shape[i]))
            biases = np.random.uniform(-1, 1, shape[i + 1])
            self.layers.append((weights, biases))

    def forward_propagation(self, X):
        """Compute the output of the network for the given input X."""
        for layer in self.layers[:-1]:
            X = np.dot(layer[0], X) + layer[1]
            X = np.maximum(0, X)  # ReLU activation

        # The output layer do not need activation
        X = np.dot(self.layers[-1][0], X) + self.layers[-1][1]

        return X
