import gym
import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import SGDRegressor
import itertools
import sys
import sklearn.pipeline
import sklearn.preprocessing

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


env = gym.envs.make("CartPole-v1")

from sklearn.kernel_approximation import RBFSampler


observation_examples = np.array([env.observation_space.sample() for x in range(10000)])

## the sampler can approximate the shape of the environment from samples
# scaler = sklearn.preprocessing.StandardScaler()
# scaler.fit(observation_examples)

featurizer = sklearn.pipeline.FeatureUnion([
        ("rbf1", RBFSampler(gamma=5.0, n_components=100)),
        ("rbf2", RBFSampler(gamma=2.0, n_components=100)),
        ("rbf3", RBFSampler(gamma=1.0, n_components=100)),
        ("rbf4", RBFSampler(gamma=0.5, n_components=100))
        ])

featurizer.fit(observation_examples)
