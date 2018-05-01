from agent import Agent
from environment import Environment
import numpy as np
from elements import Action

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

        self.N = self.get_clear_tensor()

        self.G_s = np.zeros([self.env.dealer_max_value + 1,
                             self.env.agent_max_value + 1])


    def get_value_function(self):
        return self.V


    def predict(self, episode):
        "code for MC"
        pass
    
    def policy(self):
        if self.env._game_state._player_sum >= 17:
            action = Action.STICK
            index = 0
        else:
            action = Action.HIT
            index = 1

        self.N[self.env._game_state._dealer._total][self.env._game_state._player_sum][index] += 1
        return action        

    
    def train(self, steps):
        for e in range(steps):
            env.reset_game()
            episode = []

            while not env._game_state._is_terminal:
                current_game_state = self.env._game_state
                action = self.policy()
                reward = self.env.step(action)
                episode.append((env._game_state, action, reward))

            print("Episode " + str(e) +  " complete")
            self.predict(episode)

        return self.get_value_function()


env = Environment()
agent = MCAgent(env)
value_function = agent.train(10000)
