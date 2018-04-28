
from action import Action

__author__ = "Sreejith Sreekumar"
__email__ = "sreejith.sreekumar@fmr.com"
__version__ = "0.0.1"


class Agent:

    def policy(self, s):
        return Action._HIT


class Dealer:

    def policy(self, s):
        if s._dealer_sum >= 17:
            return Action._STICK
        else:
            return Action._HIT
