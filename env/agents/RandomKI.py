from .Player import Player
import random

class RandomKI(Player):
    def get_move(self, board_size):
        x_value = random.randint(0,board_size-1)
        y_value = random.randint(0,board_size-1)

        return x_value, y_value