import gym
import numpy as np
from matplotlib import pyplot as plt

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


env = gym.envs.make("MountainCar-v0")


## rendering the mountain cart
env.reset()
plt.figure()
plt.imshow(env.render(mode='rgb_array'))

[env.step(0) for x in range(100000)]
plt.figure()
plt.imshow(env.render(mode='rgb_array'))

env.render()

