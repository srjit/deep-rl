import numpy as np
from environment import BlackJackEnv, Action

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


class MCControl:

    
    def __init__(self, gamma):

        self.gamma = gamma
        self.set_parameters()
        self.wins = 0
        self.iterations = 0

    def set_parameters(self):
        dealer_max_value = 11
        player_max_value = 22
        actions_count = 2
        self.No = 100
        self.Q = np.zeros([dealer_max_value, player_max_value, actions_count])
        self.N = np.zeros([dealer_max_value, player_max_value, actions_count])


    def get_e(self, state):
        return self.No/((self.No + sum(self.N[state.dealer_sum, state.player_sum, :]) * 1.0))

    def choose_random_action(self):
        return Action.HIT if np.random.random() <= 0.5 else Action.STICK

    def choose_best_action(self, state):
        return Action.HIT if np.argmax(self.Q[state.dealer_sum][state.player_sum]) == 1 else Action.STICK        

    def policy(self, state):
        r = np.random.random()
        if r <= self.get_e(state):
            action = self.choose_random_action()
        else:
            action = self.choose_best_action(state)
        return action

    
    def control(self, states):

        for index, state in enumerate(states):

            dealer_sum, player_sum, action, reward = state.dealer_sum, state.player_sum, state.action, state.reward

            # previous reward ? + gamma ()
            Gt = sum([_state.reward * (self.gamma**i) for i, _state in enumerate(states[index:])])

            self.N[dealer_sum][player_sum][action.value] += 1
            error = Gt - self.Q[dealer_sum][player_sum][action.value]

            _N = 1/self.N[dealer_sum][player_sum][action.value]
            self.Q[dealer_sum][player_sum][action.value] += (1/_N) * error
            


    def train(self, iterations):

        for e_idx in range(1, iterations+1):

            episode = []
            env = BlackJackEnv()

            while not env.current_state.is_terminal:
                action = self.policy(env.current_state)
                env.step(action)

            final_reward = env.game_states[-1].reward

            self.control(env.game_states)

            if final_reward == 1:
                self.wins += 1

            if e_idx % 1000 == 0:
                print("% wins after " + str(e_idx) + " games: " + str(float(self.wins)/e_idx))


## Let's run this mofo
agent = MCControl(0.1)
agent.train(10000)
