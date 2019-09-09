import gym
from gym import wrappers
from Agent import Agent
from platypus import Problem, Solution, FixedLengthArray
import platypus
import numpy as np
import copy
import time


class Trainer():
    def __init__(self, env_name, video=False):
        self.env = gym.make(env_name)
        self.env = wrappers.Monitor(self.env, 'video', video_callable=video ,force=True)
        self.env.reset()
        self.weights = [-2.0, -1.5, -1.0, -.5, .5, 1.0, 1.5, 2.0]

    def run(self, agents, runs=100000):
        for w in self.weights:
            self.simulate(w, agents, runs)
        return agents

    def simulate(self, weight, agents, runs):
        for a in agents:
            observation = self.env.reset()
            for i in range(runs):
                action = int(round(self._sigmoid(a.forward(weight, observation)[0])))
                observation, reward, done, _ = self.env.step(action)
                if done:
                    a.performance[weight] = i
                    break
        return agents

    def _sigmoid(self, x):
        if x < -10:
            return 0
        if x > 10:
            return 1
        return 1 / (1 + np.exp(-1 * x))

t = Trainer('CartPole-v0')
agents = [Agent(4, 1) for i in range(1000)]

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
    print("Generation: {} finished in {} seconds\nBest Score {}".format(generation,time.time() - start,top_score))
