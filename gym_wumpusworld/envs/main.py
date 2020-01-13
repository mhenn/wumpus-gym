import sys
import os

sys.path.append(os.getcwd())

from WumpusGym import WumpusWorldEnv


def main():
    episodes = 2
    env = WumpusWorldEnv()
    print(env.reset())
    done = False

    for e in range(episodes):
        while not done:
            env.render()
            a = int(input())
            obs, reward, done, i = env.step(a)
        env.reset()


main()
