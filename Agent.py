from platypus import Problem, Solution, FixedLengthArray
import platypus
import numpy as np
from toposort import toposort_flatten
import copy

class Agent(Solution):
    def __init__(self, input_size, output_size, *args, **kwargs):
        super(Agent, self).__init__(*args, **kwargs)
        self.input_size = input_size
        self.output_size = output_size

        self.activations = {
            'linear': lambda x: x,
            'sigmoid': lambda x: 1 / (1 + np.exp(-1 * x)),
            'tanh': lambda x: np.tanh(x),
            'relu': lambda x: np.max(0, x),
            'gaussian': lambda x: (1 / np.sqrt(2 * np.pi)) * np.exp((-1 * np.power(x, 2)) / 2),
            'step': lambda x: 1 if x >= 0 else 0,
            'sin': lambda x: np.sin(x),
            'cos': lambda x: np.cos(x),
            'inverse': lambda x: 1 / x,
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
        connected = False
        while not connected:
            choices = sorted(list(self.nodes))
            connection_from = np.random.choice(choices, 1)[0]
            connection_to = np.random.choice(choices[self.input_size:], 1)[0]

            graph_copy = copy.deepcopy(self.graph)

            if connection_from in graph_copy[connection_to]:
                continue
            graph_copy[connection_to].add(connection_from)

            try:
                toposort_flatten(graph_copy)
                self.graph[connection_to].add(connection_from)
                connected = True
            except:
                continue

agent = Agent(30, 5, Problem(1, 3))
print(agent.graph)
agent.add_connection()
print(agent.graph)
