import numpy as np

# Begin input
inputs = [
    [0, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [1, 1, 1, 0]
]

# Antwoord
labels = [0, 0, 1, 1, 1]

# Hoe die ding eruit ziet
input_nodes = 4
hidden_nodes = 3
output_nodes = 1
learning_rate = 0.1

# Willekeurig zaadje
np.random.seed(5)

weights_input_hidden = np.random.randn(input_nodes, hidden_nodes)
weights_hidden_output = np.random.randn(hidden_nodes, output_nodes)

bias_hidden = np.zeros(hidden_nodes)
bias_output = np.zeros(output_nodes)

# Getalletje tussen 0 en 1
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Afgeleide van sigmoid (voor backpropagation)
def sigmoid_derivative(x):
    return x * (1 - x)

# Feedforward-functie
def feedforward(input_vector):
    hidden_input = [0] * hidden_nodes
    for j in range(hidden_nodes):
        for i in range(input_nodes):
            hidden_input[j] += input_vector[i] * weights_input_hidden[i][j]
        hidden_input[j] += bias_hidden[j]

    hidden_output = [sigmoid(x) for x in hidden_input]

    final_input = 0
    for j in range(hidden_nodes):
        final_input += hidden_output[j] * weights_hidden_output[j][0]
    final_input += bias_output[0]

    final_output = sigmoid(final_input)

    return hidden_output, final_output

# Backpropagation + training
for epoch in range(1000):
    total_error = 0

    for index in range(len(inputs)):
        x = inputs[index]
        y = labels[index]

        # Feedforward
        hidden_out, pred = feedforward(x)

        # Error berekening (kwadratische fout)
        error = y - pred
        total_error += error**2

        # Output -> hidden update
        delta_output = error * sigmoid_derivative(pred)

        for j in range(hidden_nodes):
            weights_hidden_output[j][0] += learning_rate * delta_output * hidden_out[j]

        bias_output[0] += learning_rate * delta_output

        # Hidden -> input update
        delta_hidden = [0] * hidden_nodes
        for j in range(hidden_nodes):
            delta_hidden[j] = delta_output * weights_hidden_output[j][0] * sigmoid_derivative(hidden_out[j])
            for i in range(input_nodes):
                weights_input_hidden[i][j] += learning_rate * delta_hidden[j] * x[i]
            bias_hidden[j] += learning_rate * delta_hidden[j]

    # Print elke 100 iteraties de totale fout
    if epoch % 100 == 0:
        print(f"Epoch {epoch} - Total Error: {total_error}")
