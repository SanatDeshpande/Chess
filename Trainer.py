import gym
from gym import wrappers

class Trainer():
    def __init__(self, env_name, video=False):
        self.env = gym.make(env_name)
        self.env = wrappers.Monitor(self.env, 'video', video_callable=video ,force=True)
        self.env.reset()

    def run(self, agents, runs=100000):
        for a in agents:
            observation = self.env.reset()
            for i in range(runs):
                action = a.react(observation)
                observation, reward, done, _ = self.env.step(action)
                if done:
                    a.performance = reward
                    break
        return agents
