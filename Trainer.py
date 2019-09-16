import gym
from gym import wrappers
from Agent import Agent
from platypus import Problem, Solution, FixedLengthArray
import platypus
import numpy as np
import copy
import time
from TicTacToe import TicTacToe


class Trainer():
    def __init__(self, game):
        self.game_class = game
        self.game = self.game_class() #initializes game
        self.weights = [-2.0, -1.5, -1.0, -.5, .5, 1.0, 1.5, 2.0]

    def run(self, agents):
        for w in self.weights:
            self.simulate(w, agents)
        return agents

    def simulate(self, weight, agents, max_length=1000, num_games=10):
        for count, a in enumerate(agents):
            rewards = 0
            for n in range(num_games):
                for i in range(max_length):
                    state = self.game.get_state()
                    action = a.forward(weight, state)
                    reward = self.game.step(action)
                    if reward == -1 or reward == 1:
                        break
                rewards += reward
                self.game = self.game_class()
            a.performance[weight] = rewards
        return agents

agents = [Agent(9, 2) for i in range(100)]
top_agent = None
t = Trainer(TicTacToe)

for generation in range(100):
    start = time.time()
    agents = t.run(agents)

    for count, a in enumerate(agents):
        avg = sum([v for k, v in a.performance.items()]) / len(a.performance)
        top = max([v for k, v in a.performance.items()])
        agents[count].criterion = (avg, top)

    agents.sort(key=lambda x: x.criterion[0] if np.random.random() < 0 else x.criterion[1])
    agents = agents[-90:] + agents[:10]

    population = []
    for i in range(10):
        population.append(copy.deepcopy(agents))
        for count, p in enumerate(population[-1]):
            population[-1][count].mutate()

    agents = []
    for p in population:
        agents += p

    top_score = max([a.criterion[1] for a in agents])
    avg_score = np.mean([a.criterion[1] for a in agents])
    print("Generation: {} finished in {} seconds\nBest Score {}\nAvg Score {}".format(generation,time.time() - start,top_score, avg_score))


    top_agent = agents[np.argmax([a.criterion[1] for a in agents])]
