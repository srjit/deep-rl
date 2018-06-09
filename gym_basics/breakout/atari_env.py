import gym
import numpy as np
import matplotlib.pyplot as plt

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"

env = gym.envs.make("Breakout-v0")
#
#print(env.get_action_meanings())

print("Actions:", env.action_space)
observation = env.reset()

plt.figure()
plt.imshow(env.render(mode='rgb_array'))

plt.show()
