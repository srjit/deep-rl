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

    def __init__(self, player_sum, dealer, is_terminal):
        self._player_sum = player_sum
        self._dealer = dealer
        self._is_terminal = is_terminal

    def __str__(self):
        return "{ Player Sum: " + str(self._player_sum) + "," +\
            " Dealer Sum: " + str(self._dealer._total) + "," +\
            " Is Terminal: " + str(self._is_terminal) + "," +\
            "}"


class Environment:

    def __init__(self):
        '''
        Do not touch the deck and dealer directly
        '''
        self.reset_game()

        self.agent_max_value = 21
        self.dealer_max_value = 21
        self.actions_count = 2

    def reset_game(self):
        self._deck = Deck()
        self._dealer = Dealer()
        
        initial_player_sum = 0
        self._game_state = GameState(initial_player_sum,
                                     self._dealer,
                                     False)
        
        card_for_dealer = self._deck.pick_starting_black_card()
        card_for_player = self._deck.pick_starting_black_card()

        print("Agent received an initial black card with value ",
              card_for_player._value)
        print("Dealer received an initial black card with value ",
              card_for_dealer._value)

        self._game_state._dealer._total = card_for_dealer._value
        self._game_state._player_sum = card_for_player._value

    def check_bust(self, is_agent=False):
        if is_agent:
            return self._game_state._player_sum > 21 or \
                self._game_state._player_sum <= 1

        return self._game_state._dealer._total > 21 or \
            self._game_state._dealer._total <= 1

    def _add_card_value(self, card, is_agent=False):
        value = 0
        if card._color == Color.BLACK:
            value = card._value
        else:
            value = -1 * card._value

        if is_agent:
            self._game_state._player_sum += value
        else:
            self._game_state._dealer._total += value

    def _make_dealer_moves(self):
        action = None

        while not self._game_state._is_terminal and action != Action.STICK:
            action = self._game_state._dealer._policy()
            if action == Action.HIT:
                card = self._deck.pick_card()
                print("Dealer picked: ", card)
                self._add_card_value(card)
            self._game_state._is_terminal = self.check_bust()

    def _check_higher_total_and_give_reward(self):
        if self._game_state._player_sum > self._dealer._total:
            return 1
        elif self._game_state._player_sum == self._dealer._total:
            return 0
        else:
            return -1

    def step(self, player_action):

        reward = 0
        if player_action == Action.STICK:
            # Player stopped playing. Now the dealer makes moves
            self._make_dealer_moves()
            if self._game_state._is_terminal:
                reward = 1
            else:
                reward = self._check_higher_total_and_give_reward()
                self._game_state._is_terminal = True

        # player has to play now
        else:
            card = self._deck.pick_card()
            self._add_card_value(card, is_agent=True)
            self._game_state._is_terminal = self.check_bust(is_agent=True)
            if self._game_state._is_terminal:
                reward = -1

        return reward


# --------  Testing -------- #
# (Yes, I know...But I don't have time for a proper test suite)

# Creating the environment
#env = Environment()

# Checking the dealer moves
# env._make_dealer_moves()

# player is not playing
# if the dealer crosses 21 or falls below -1 player wins
# if the dealer stops between 17 and 21, he wins since the
# player is not playing and only maintains his initial sum of 0

#reward = env.step(Action.STICK)
