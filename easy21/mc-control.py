from agent import Agent
from environment import Environment
import numpy as np
from elements import Action
import copy

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


# Control for the Monte Carlo agent
# ToDo


class MCControl(Agent):

    def __init__(self, environment, gamma, No=100):
        Agent.__init__(self, environment, gamma, No)

        self.N = self.get_clear_tensor()

        self.Gs = np.zeros([self.env.dealer_max_value + 1,
                            self.env.agent_max_value + 1])
