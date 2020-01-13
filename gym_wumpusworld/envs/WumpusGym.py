import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_wumpusworld.envs.WumpusWorld import Wumpus_World
from gym_wumpusworld.envs.WorldState import World_State, Action


class WumpusWorldEnv(gym.Env):
    metadata = {'render.modes' : ['human']}
    def __init__(self, size=4):
        self._world = Wumpus_World(size)
        self.action_space = [0,1,2,3,4,5]

    def step(self, action):
        done = self._world.exec_action(action)
        obs = self._world.get_observation()
        reward = self._world.get_reward()
        return obs, reward, not done, {"info", "no further information"}

    def reset(self):
        self._world.reset()
        return self._world.get_observation()

    def render(self, mode='human'):
        self._world.print()

    def close(self):
        print("Not necessary since no seperate window was opened")
        pass
