from agent import Agent
from environment import Environment
import numpy as np
from elements import Action
import copy

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


# Pseudo code of the MCPE
#  for i in iterations_limit:
#     n(s) <- n(s) + 1
#     G_s(s) <- G_s(s) + Gt    ## Total value received until now
#     V(s) <- S(s)/n(s)

class MCAgent(Agent):

    def __init__(self, environment, gamma, No=100):
        Agent.__init__(self, environment, gamma, No)

        self.N = self.get_clear_tensor()

        self.Gs = np.zeros([self.env.dealer_max_value + 1,
                            self.env.agent_max_value + 1])

    def predict(self, episode):
        '''
        Calculating the predicted return for each game state in the episode
        
        Value function approximation - this prediction has to improve over
        time
        '''
        import ipdb
        ipdb.set_trace()
        for index, (state, action, reward) in enumerate(episode):
            
            # find the return - Gt: Notation like how Dr.Silver uses it
            Gt = sum([(self._gamma**idx)*_reward for idx, (_, _, _reward) in
                  enumerate(episode[index:])])

            # for each dealer sum agent sum combination,
            # how much reward am I getting?
            self.Gs[state._dealer._total][state._player_sum] += Gt

            # average reward for a particular action at a particular
            # value of dealer sum and agent sum
            self.V[state._dealer._total][state._player_sum] = self.Gs[state._dealer._total][state._player_sum] / sum(
                self.N[state._dealer._total, state._player_sum, :])

            import ipdb
            ipdb.set_trace()

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
            try:
                self.predict(episode)
            except Exception:
                print("Dealer sum above 21, Skipping this episode for now")

        return self.V


env = Environment()
agent = MCAgent(env, gamma=0.1)
value_function = agent.train(10000)
