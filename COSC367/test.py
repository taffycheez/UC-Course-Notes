from abc import abstractmethod, ABCMeta
import numpy as np

class Function(metaclass=ABCMeta):

    @abstractmethod
    def __call__(self, inputs):
        """Uses the call operator so the layer can be called like an ordinary function.
        The method takes a vector (numpy array, list, etc) of numbers and must returns the
        vector of values resulting from function the layer is implementing."""

class ReLU(Function):
    def __call__(self, inputs):
        result = []
        for i in inputs:
            if i < 0:
                result.append(0)
            else:
                result.append(i)
        self.cache = np.array(result)
        return np.array(result)
    
class Sigmoid(Function):
    def __call__(self, inputs):
        result = np.array(1/(1+np.exp(-inputs)))
        self.cache = result
        return result

class Linear(Function):
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias
        
    def __call__(self, inputs):
        result = np.matmul(self.weights, inputs) + self.bias
        self.cache = result
        return result

def forward_pass(functions, input_vector):
    x = input_vector
    for f in functions:
        x = f(x)
    return x

layer = Linear(
    np.array([[2.0, 0.0, 1.0], [0.0, -1.0, 3.0]]),
    np.array([1.0, 0.5])
)
input_vector = np.array([1.0, -1.0, -1.0])
functions = [layer, ReLU()]
z = forward_pass(functions, input_vector)
print(input_vector, '->', layer.cache, '->', z)