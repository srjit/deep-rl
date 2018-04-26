import players

__author__ = "Sreejith Sreekumar"
__email__ = "sreejith.sreekumar@fmr.com"
__version__ = "0.0.1"


class Environment():

    def __init__(self):
        self._agent = players.Agent()
        self._dealer = players.Dealer()

    def check_if_busted(self, player_sum):
        return player_sum > 21 or player_sum < 1

    def reward_if_busted(self, s):
        if s._agent_sum > s._dealer_sum:
            return 1
        elif s._agent_sum == s.dealer_sum:
            return 0
        else:
            return -1
