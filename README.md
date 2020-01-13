This repository contains a PIP package which is an OpenAI environment for
simulating an wumpusworld environment.


## Installation

Install the [OpenAI gym](https://gym.openai.com/docs/).

Then install this package via

```
pip install -e .
```

## Usage

```
import gym
import gym_wumpusworld

env = gym.make('Wumpus-v0')
```
