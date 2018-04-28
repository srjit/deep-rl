from elements import Action
import random

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"

class Agent():

    def __init__(self, environment, No=100, discount_factor=1):

        self.env = environment

        # let's figure this out later
        self.No = No
        self.discount_factor = discount_factor

        # the state value function -  how good is it to be in a state
        self.V = np.zeros([self.env.dealer_max_value + 1, self.env.agent_max_value + 1])

        self.wins = 0.0
        self.iterations = 0.0        


        
    def policy(self):
        return Action.HIT


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
        for i in xrange(1, self.env.dealer_max_value + 1):
            for j in xrange(1, self.env.agent_max_value + 1):
                s = State(i, j)
                self.V[i][j] = self.get_max_action(s)
        return self.V
    

    

        
