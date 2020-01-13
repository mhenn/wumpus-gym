from gym.envs.registration import register

register(
        id='Wumpus-v0',
        entry_point='gym_wumpusworld.envs:WumpusWorldEnv',
        )
