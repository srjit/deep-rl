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
        self.Ns = self.get_clear_tensor()
        

    def epsilon(self, state):
        return self.No/((self.No + sum(self.Ns[state._dealer._total, state._player_sum, :])) * 1.0)

    
    def alpha(self, state, action):
        return 1.0/(self.Ns[state._dealer._total_sum][state._player_sum][action.value])

    def get_max_action(self, state):
        if np.max(self.Q[state._dealer._total][state._player_sum]) == 0:
            return Action.STICK
        return Action.HIT
        
    def policy(self, state):
        '''
        At each state what is the best policy
        
        What action should i take
        if value of the random is less than epsilon, explore
        else exploit
        '''
        r = np.random.rand()
        if r < self.epsilon(state):
            action = self.choose_random_action()
        else:
            action = self.choose_best_action(state)

        return action

    
    def control(self, episode):
        '''
        Improve the approximation of Q(s,a) towards Bellman optimal Action value function
        Q*(s, a)
        '''
        i = 0
        for index, (state, action, reward) in enumerate(episode):
            Gt = sum([(self._gamma**idx)*_reward for idx, (_, _, _reward) in
                  enumerate(episode[index:])])
            self.Ns[self._dealer._total][self._player_sum] += 1

            error = Gt - self.Q[self._dealer._total][self._player_sum][action.value]

            self.Q[self._dealer._total][self._player_sum][action.value] += self.alpha(state, action) * error
            i += 1
            

    def train(self, steps):

        for episode_id, e in enumerate(range(steps)):
            # print("Beginning episode ", episode_id)
            episode = []
            env.reset_game()

            reward = 0

            while not env._game_state._is_terminal:
                current_game_state = copy.copy(self.env._game_state)
                
                action = self.policy(current_game_state)
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

            # print("Episode " + str(e) + " complete")

            if reward == 1:
                self.wins += 1
            
            if episode_id % 1000 == 0:
                # import ipdb
                # ipdb.set_trace()
                print("Win Percentage:", (float(self.wins)/(episode_id+1))*100.0)
            
        return self.V
        

env = Environment()
agent = MCAgentControl(env, gamma=0.1)
value_function = agent.train(100000)
    
