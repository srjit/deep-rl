from agent import Agent
from environment import Environment
import numpy as np
from elements import Action
import copy


__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


class MCAgentControl(Agent):

    def __init__(self, environment, gamma, No=100):


        Agent.__init__(self, environment, gamma, No)

        # action value function - three dimensions
        # a) Dealer Sum Value
        # b) Agent Sum Value
        # c) Possible Actions 
        self.Q = self.get_clear_tensor()

        # N(s) - number of times a state has been visited
        # N(s,a) - number of times a state has been selected
        # and an action has been chosen
        self.Ns = np.zeros([self.env.dealer_max_value + 1,
                            self.env.agent_max_value + 1])


    def epsilon(self):
        return self.No/((self.No + sum(self.N[state._dealer._total_sum, state._player_sum, action.value])) * 1.0))        

    
    def alpha(self,state,action):
        return 1.0/(self.N[state._dealer._total_sum][state._player_sum][action.value])

    def get_max_action(self, state):
        return np.max(self.Q[state._dealer._total][state._player_sum])
        

    def policy(self, state):
        '''
        At each state what is the best policy
        
        What action should i take
        if value of the random is less than epsilon, explore
        else exploit
        '''
        r = np.random.rand()
        if r < self.epsilon():
            action = self.choose_random_action()
        else:
            action = self.choose_best_action(state)

        return action

    
    def control(self):
        '''
        Improve the approximation of Q(s,a)
        '''
        pass

    def train(self):

        for episode_id, e in enumerate(range(steps)):
            print("Beginning episode ", episode_id)
            episode = []
            env.reset_game()

            reward = 0

            while not env._game_state._is_terminal:
                current_game_state = copy.copy(self.env._game_state)
                
                action = self.policy()
                reward = self.env.step(action)

                # the 'if' statement is a hack
                # if the score of the dealer goes above 21 and game state
                # is not termial - why does this happen - is there a bug?

                # we need to create a copy of the game state to append
                # to the episode if we don't, we'll be getting only the
                # final state of the game state since they are all pointers
                # to the same object
                if current_game_state._dealer._total <= 21:
                    episode.append((current_game_state, action, reward))

            print("Episode " + str(e) + " complete")

            if reward == 1:
                self.wins += 1
            
            if episode_id % 10000 == 0 and self.iterations > 0:
                print("Win Percentage:", (float(self.wins)/e)*100.0)
            
        return self.V
        
