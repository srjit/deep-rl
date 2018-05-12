import numpy as np
from enum import Enum
import copy

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"

class Action(Enum):

    STICK = 0,
    HIT = 1


class Color(Enum):
    
    RED = 0,
    BLACK = 1

    
class Card:

    def __init__(self, _color=None):
        self.value = self._get_value()
        self.color = self._get_color() if _color is None else _color

    def _get_value(self):
        return np.random.randint(1,10)

    def _get_color(self):
        r = np.random.random()
        if r <= 0.3:
            return Color.RED
        else:
            return Color.BLACK


class Deck:

    def draw_random_card(self):
        return Card()
        
    def draw_black_card(self):
        return Card(Color.BLACK)


class Dealer:

    def  policy(self, current_total):
        if current_total >= 17:
            return Action.STICK
        return Action.HIT
        
        
class State:

    def __init__(self, _dealer_sum, _player_sum, _reward, _is_terminal):
        self.dealer_sum = _dealer_sum
        self.player_sum = _player_sum
        self.reward = _reward
        self.is_terminal = _is_terminal

    def __str__(self):
        return "{" +\
            " Agent Sum: " + str(self.player_sum) + "," +\
            " Dealer Sum: " + str(self.dealer_sum) + "," +\
            "Reward:" + str(self.reward) + "," +\
            " Is Terminal: " + str(self.is_terminal) +\
            "}"
        
    
class BlackJackEnv:

    def  __init__(self):
        self.reset_game()

    def reset_game(self):
        self.deck = Deck()
        self.dealer = Dealer()

        initial_dealer_sum = self.deck.draw_black_card().value
        initial_player_sum = self.deck.draw_black_card().value
        
        self.current_state = State(initial_dealer_sum, initial_player_sum, 0, False)

        _tmp = copy.copy(self.current_state)

        self.game_states = [_tmp]


    def has_player_lost(self, new_player_sum):
        if new_player_sum > 21 or new_player_sum < 1:
            return True
        return False


    def has_dealer_lost(self, new_dealer_sum):
        if new_dealer_sum > 21 or new_dealer_sum < 1:
            return True
        return False


    def reward(self, dealer_sum, player_sum, is_terminal):
        if self.has_dealer_lost(dealer_sum):
            return 1
        elif is_terminal:
            if dealer_sum > player_sum:
                return -1
            elif player_sum > dealer_sum:
                return 1
            else:
                return 0
        return 0


    def get_effective_card_value(self, card):
        if card.color == Color.RED:
            return -1 * card.value
        return card.value


    def play_dealer_moves(self):
        action = self.dealer.policy(self.current_state.dealer_sum)
        if action == Action.HIT:
            value = self.get_effective_card_value(self.deck.draw_random_card())
            dealer_sum = self.current_state.dealer_sum + value
            player_sum = self.current_state.player_sum
            is_terminal = self.has_dealer_lost(dealer_sum)
        else:
            dealer_sum = self.current_state.dealer_sum
            player_sum = self.current_state.player_sum
            is_terminal = True

        reward = self.reward(dealer_sum, player_sum, is_terminal)

        self.current_state = State(dealer_sum, player_sum, reward, is_terminal)
        self.game_states.append(self.current_state)

        if not is_terminal:
            self.play_dealer_moves()

            
    def step(self, player_action):
        r = 0
        if player_action == Action.HIT:
            value = self.get_effective_card_value(self.deck.draw_random_card())
            print("--->", value)
            dealer_sum = self.current_state.dealer_sum
            player_sum = self.current_state.player_sum + value
            is_terminal = self.has_player_lost(player_sum)
            reward = self.reward(dealer_sum, player_sum, is_terminal)
            self.current_state = State(dealer_sum,
                                       player_sum,
                                       reward,
                                       is_terminal)
            self.game_states.append(self.current_state)
        else:
            self.play_dealer_moves()

