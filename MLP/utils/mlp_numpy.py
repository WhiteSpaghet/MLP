# utils/mlp_numpy.py
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)

class Neuron:
    def __init__(self, n_inputs, activation='sigmoid'):
        self.weights = np.random.randn(n_inputs) * 0.01
        self.bias = 0.0
        self.activation_name = activation
        if activation == 'sigmoid':
            self.activation = sigmoid
        elif activation == 'relu':
            self.activation = relu
        else:
            raise ValueError(f"Unsupported activation: {activation}")

    def forward(self, x):
        z = np.dot(x, self.weights) + self.bias
        return self.activation(z)

class Layer:
    def __init__(self, n_inputs, n_neurons, activation='sigmoid'):
        self.neurons = [Neuron(n_inputs, activation) for _ in range(n_neurons)]

    def forward(self, X):
        return np.array([neuron.forward(X) for neuron in self.neurons]).T

class MLP:
    def __init__(self, layer_sizes, activations):
        """
        layer_sizes: lista de tamaño de capas, ej. [784, 128, 64, 10]
        activations: lista de activaciones para cada capa (excepto entrada)
        """
        self.layers = []
        for i in range(1, len(layer_sizes)):
            self.layers.append(Layer(layer_sizes[i-1], layer_sizes[i], activations[i-1]))

    def predict(self, X):
        out = X
        for layer in self.layers:
            out = layer.forward(out)
        return out
