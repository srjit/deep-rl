from elements import Color, Deck, Action, Dealer

__author__ = "Sreejith Sreekumar"
__email__ = "sreejith.sreekumar@fmr.com"
__version__ = "0.0.1"

# things to program
# Strategy of the dealer
# Elements Required - 1) Sum of Cards currently holding
#                     2) A deck to pick a card from
#

class GameState:

    def __init__(self, player_sum, dealer_sum, is_terminal):
        self._player_sum = player_sum
        self._dealer_sum = dealer_sum
        self._is_terminal = is_terminal


class Environment:

    def __init__(self):
        self._deck = Deck()
        self._dealer = Dealer()
        self._player_sum = 0
        self._is_terminal = False
        self.game_state = GameState(self._player_sum,
                                    self._dealer._total,
                                    self._is_terminal)
        self.collect_initial_cards()
        
        

    def collect_initial_cards(self):
        card_for_dealer = self._deck.pick_starting_black_card()
        card_for_player = self._deck.pick_starting_black_card()

        self._dealer._total += card_for_dealer._value
        self._player_sum += card_for_player._value
        

        
    
    def game_state(self):
        return self.game_state

    
    def check_bust(self, is_agent=False):
        if is_agent:
            return self._player_sum > 21 or self._player_sum <= 1
        
        return self._dealer._total > 21 or self._dealer._total <= 1
        

    def _add_card_value(self, card, is_agent=False):
        value = 0
        if card._color == Color.BLACK:
            value = card._value
        else:
            value = -1 * card._value

        if is_agent:
            self._player_sum += value
        else:
            self._dealer._total += value
        
        
    def _make_dealer_moves(self):
        
        action = None
        dealer_sum = 0
        
        while not self._is_terminal and action != Action.STICK:
            action = self._dealer._policy()
            if action == Action.HIT:
                card = self._deck.pick_card()
                self._add_card_value(card)
            self._is_terminal = self.check_bust()


    def _check_higher_total_and_give_reward(self):
        if self._player_sum > self._dealer._total:
            return 1
        elif self._player_sum == self._dealer._total:
            return 0
        else:
            return -1
        
        
    def step(self, player_action):

        if player_action == Action.STICK:
            # Player stopped playing. Now the dealer makes moves
            next_state = self._make_dealer_moves()
            if self._is_terminal:
                reward = 1
            else:
                reward = self._check_higher_total_and_give_reward()
                self._is_terminal = True

        # player has to play now
        else:
            card = self._deck.pick_card()
            self._add_card_value(card, is_agent=True)
            self._is_terminal = self.check_bust(is_agent=True)
            if self._is_terminal:
                reward = -1

        return reward

                
        # else:
            # Player plays
        # next_state = self._deck.pick_card()
            

env = Environment().step(Action.STICK)
