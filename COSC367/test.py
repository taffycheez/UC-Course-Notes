def construct_perceptron(weights, bias):
    """Returns a perceptron function using the given paramers."""
    def perceptron(input):
        result = 0
        for i in range(len(input)):
            result += input[i] * weights[i]
        result += bias      
        return int(result >= 0)
    
    return perceptron # this line is fine
    
def accuracy(classifier, inputs, expected_outputs):
    correct = 0
    for i in range(len(inputs)):
        if classifier(inputs[i]) == expected_outputs[i]:
            correct += 1
    return correct / len(inputs)

def learn_perceptron_parameters(weights, bias, training_examples, learning_rate, max_epochs):
    
    for _ in range(max_epochs):
        weights_prev, bias_prev = weights.copy(), bias
        
        for x, y in training_examples:
            perceptron = construct_perceptron(weights, bias)
            pred = perceptron(x)
            for i in range(len(x)):
                weights[i] += learning_rate*x[i]*(y-pred)
            bias += learning_rate*(y-pred)
        
        if weights == weights_prev and bias == bias_prev:
            break
        
    return (weights, bias)

weights = [2, -4]
bias = 0
learning_rate = 0.5
examples = [
  ((0, 0), 0),
  ((0, 1), 1),
  ((1, 0), 1),
  ((1, 1), 0),
  ]
max_epochs = 50

weights, bias = learn_perceptron_parameters(weights, bias, examples, learning_rate, max_epochs)
print(f"Weights: {weights}")
print(f"Bias: {bias}\n")