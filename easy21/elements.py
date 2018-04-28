import random
from enum import Enum

__author__ = "Sreejith Sreekumar"
__email__ = "sreejith.sreekumar@fmr.com"
__version__ = "0.0.1"


class Action(Enum):

    STICK = "_stick"
    HIT = "_hit"


class Color(Enum):

    RED = "_red"
    BLACK = "_black"


class Card:

    def __init__(self):
        self._color = self._get_color()
        self._value = self._get_value()

    def _get_color(self):
        r = random.random()
        if r <= 0.3:
            return Color.RED
        else:
            return Color.BLACK

    def _get_value(self):
        return random.randint(1, 10)


class Deck:

    def pick_card(self):
        return Card()


class Dealer:

    def __init__(self):
        self._total = 0

    def _policy(self):
        if self._total >= 17:
            return Action.STICK
        else:
            return Action.HIT

