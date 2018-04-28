from agent import Agent

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


# Pseudo code of the MCPE
#  for i in iterations_limit:
#     n(s) <- n(s) + 1
#     G_s(s) <- G_s(s) + Gt    ## Total value received until now
#     V(s) <- S(s)/n(s)

class MCAgent(Agent):

    def __init__(self, environment, No=100, discount_factor=100):
        Agent.__init__(self, environment, No, discount_factor)
        self.G_s = np.zeros([self.env.dealer_max_value + 1, self.env.agent_max_value + 1])


    def get_value_function(self):
        return self.V

    def policy(self):
        pass

    def train(self, steps):

        
        for e in range(steps):
            episode = []

            while not env._game_state._is_terminal:

                current_game_state = self.env._game_state
                action = self.policy()
                reward = self.env.step(action)
                episode.append((env._game_state, action, reward))

                

                

                
   
            
            
        
