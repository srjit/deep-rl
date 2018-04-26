
import random

__author__ = "Sreejith Sreekumar"
__email__ = "sreekumar.s@husky.neu.edu"
__version__ = "0.0.1"


class Card:

    def __init__(self):
        self.color = self._get_color()
        self.number = self._get_number()
    
    
    def _get_color(self):
        random_number = random.random()
        if random_number <= 0.3:
            return "black"
        else:
            return "red"

    def _get_number(self):
        return random.random(1, 10)


    
class Deck:
    def _get_card():
        return Card()
    
        
