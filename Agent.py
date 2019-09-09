from platypus import Problem, Solution, FixedLengthArray
import platypus
import numpy as np
from toposort import toposort_flatten
import copy

class Agent():
    def __init__(self, input_size, output_size, *args, **kwargs):
        self.input_size = input_size
        self.output_size = output_size
        self.performance = {}
        self.criterion = None

        self.activations = {
            'linear': lambda x: x,
            'sigmoid': lambda x: 1 / (1 + np.exp(-1 * x)),
            'tanh': lambda x: np.tanh(x),
            'relu': lambda x: max(0, x),
            'gaussian': lambda x: (1 / np.sqrt(2 * np.pi)) * np.exp((-1 * np.power(x, 2)) / 2),
            'step': lambda x: 1 if x >= 0 else 0,
            'sin': lambda x: np.sin(x),
            'cos': lambda x: np.cos(x),
            'inverse': lambda x: 1 / (x + 1e-9),
        }

        self.nodes = {i:self.activations['linear'] for i in range(input_size)}
        for i in range(input_size, output_size + input_size):
            self.nodes[i] = self.activations['linear']

        self.graph = {i:set([]) for i in range(input_size, output_size + input_size)}

        connections_from = np.random.choice(input_size, 1 if input_size//10 == 0 else input_size//10, replace=False)
        connections_to = np.random.choice(output_size, len(connections_from), replace=True) + input_size

        for c_to, c_from in zip(connections_to, connections_from):
            self.graph[c_to].add(c_from)

    def add_connection(self):
        while True:
            input_nodes = set([i for i in range(self.input_size)])
            output_nodes = set([i for i in range(self.input_size, self.input_size + self.output_size)])
            other_nodes = set([i for i in self.nodes]).difference(input_nodes)
            other_nodes = other_nodes.difference(output_nodes)

            input_pool = input_nodes.union(other_nodes)
            output_pool = output_nodes.union(other_nodes)

            connection_from = np.random.choice(list(input_pool), 1)[0]
            if connection_from in output_pool:
                output_pool.remove(connection_from)
            connection_to = np.random.choice(list(output_pool), 1)[0]

            try:
                self.graph[connection_to].add(connection_from)
                toposort_flatten(self.graph)
                break
            except:
                self.graph[connection_to].remove(connection_from)

    def add_node(self):
        new_node = len(self.nodes)
        new_activation = np.random.choice(list(self.activations), 1)[0]
        self.nodes[new_node] = self.activations[new_activation]

        eligible = [i for i in list(self.graph) if len(self.graph[i]) > 0]
        key = np.random.choice(eligible, 1)[0]
        replaced = np.random.choice(list(self.graph[key]), 1)[0]

        self.graph[key].remove(replaced)
        self.graph[key].add(new_node)

        self.graph[new_node] = set([replaced])

    def change_activation(self):
        choice = np.random.choice(sorted(list(self.nodes)), 1)[0]
        new_activation = np.random.choice(list(self.activations), 1)[0]
        self.nodes[choice] = self.activations[new_activation]

    def mutate(self):
        mutation_list = [self.add_connection, self.add_node, self.change_activation]
        mutation = np.random.choice(mutation_list, 1)[0]
        mutation()

    def forward(self, weight, inputs):
        assert len(inputs) == self.input_size

        output_nodes = set([i for i in range(self.input_size, self.input_size + self.output_size)])
        output_nodes = list(output_nodes)
        return [self.recursive_pass(output_nodes[i], inputs) for i in range(self.output_size)]

    def recursive_pass(self, i, inputs):
        if i < self.input_size:
            return inputs[i]
        activation = self.nodes[i]
        return activation(sum([self.recursive_pass(subnode, inputs) for subnode in self.graph[i]]))
