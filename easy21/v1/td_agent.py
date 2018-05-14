from agent import Agent
from environment import Environment
import numpy as np
from elements import Action
import copy

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"

## 


class TDAgent(Agent):

    def __init__(self, environment, gamma, No=100):
        Agent.__init__(self, environment, gamma, No)

        self.N = self.get_clear_tensor()

        self.Gs = np.zeros([self.env.dealer_max_value + 1,
                            self.env.agent_max_value + 1])

    def predict(self, current_state_details,
                       next_state_details):
        '''
        Recompute reward of current state

        reducing the TD error
        
        '''
        (current_game_state, current_action, current_reward) = current_state_details
        (next_game_state, next_action, next_reward) = next_state_details
        
        Gt = self._gamma * next_reward

        self.Gs[current_game_state._dealer._total][current_game_state._player_sum] += Gt

        prev_Vs = self.V[current_game_state._dealer._total][current_game_state._player_sum]
        alpha = 1/(sum(self.N[current_game_state._dealer._total, current_game_state._player_sum, :]))

        update = alpha * ((current_reward + Gt) - prev_Vs)
        
        self.V[current_game_state._dealer._total][current_game_state._player_sum] = prev_Vs + update
        
        print("Predicted return: ", str(self.V[current_game_state._dealer._total][current_game_state._player_sum]))

            

    def policy(self):
        if self.env._game_state._player_sum >= 17:
            action = Action.STICK
            # index = Action.STICK.value
        else:
            action = Action.HIT
            # index = Action.HIT.value

        self.N[self.env._game_state._dealer._total][self.env._game_state._player_sum][action.value] += 1
        return action

    def train(self, steps):

        for episode_id, e in enumerate(range(steps)):
            print("Beginning episode ", episode_id)
            episode = []
            env.reset_game()
            
            previous_game_state = None
            previous_action = None
            previous_reward = None
            
            while not env._game_state._is_terminal:
                current_game_state = copy.copy(self.env._game_state)
                action = self.policy()
                reward = self.env.step(action)

                ## In this case we won't wait until the end of the episode
                ## to predict -

                ## we'll predict for the reward from for previous state HERE
                ## itself using the reward from the currect state 
                ## i.e previous state reward = previous state reard + gamma * reward from current state)

                if current_game_state._dealer._total <= 21:
                    episode.append((current_game_state, action, reward))

                if previous_game_state is not None:

                    try:
                        self.predict((previous_game_state, previous_action, previous_reward),
                                     (current_game_state, action, reward))
                    except:
                        print("Dealer sum above 21, Skipping...")

                previous_game_state = current_game_state
                previous = action
                previous_reward = reward
                

        return self.V


env = Environment()
agent = TDAgent(env, gamma=0.1)
value_function = agent.train(10000)
