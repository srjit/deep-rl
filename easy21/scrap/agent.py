from elements import Action
import random
import numpy as np

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


class Agent:

    def __init__(self, environment, gamma, No=100):

        self.env = environment

        # let's figure this out later
        self.No = No
        self._gamma = gamma

        # our state value function -  how good is it to be the possible states
        self.V = np.zeros([self.env.dealer_max_value + 1,
                           self.env.agent_max_value + 1])

        self.wins = 0.0
        self.iterations = 0.0

    def policy(self):
        return Action.HIT

    def get_clear_tensor(self):
        '''
        which action is the best to take when the dealer has a particular value
        and the agent has a particular value
        Syntax: (dealer_sum, agent_sum, action-to-take)
        '''
        return np.zeros((self.env.dealer_max_value + 1,
                         self.env.agent_max_value + 1,
                         self.env.actions_count))

    def choose_random_action(self):
        prob = random.random()
        if prob < 0.5:
            return Action.HIT
        return Action.STICK

    def choose_best_action(self):
        return Action.HIT

    def get_max_action(self):
        '''
        Return maxQ(s,a) between all actions
        '''
        return 0.0

    def get_best_value_function(self):
        '''
        Get the action which returns the maximum
        value among all the possible actions - for every state
        '''
        for i in range(1, self.env.dealer_max_value + 1):
            for j in range(1, self.env.agent_max_value + 1):
                s = (i, j)
                self.V[i][j] = self.get_max_action(s)
        return self.V
