from elements import Dealer
from elements import Deck

__author__ = "Sreejith Sreekumar"
__email__ = "sreejith.sreekumar@fmr.com"
__version__ = "0.0.1"

# things to program
# Strategy of the dealer
# Elements Required - 1) Sum of Cards currently holding
#                     2) A deck to pick a card from
#


class GameState:

    def __init__(self, dealer_sum=0, player_sum=0, is_terminal=False):
        self._dealer_sum = dealer_sum
        self._player_sum = player_sum
        self._is_terminal = is_terminal


class Environment:

    def __init__(self):
        self._dealer = Dealer()
        self._deck = Deck()

    def step(self, game_state, player_action):
        '''
        Given a state and action return next game state
        '''
