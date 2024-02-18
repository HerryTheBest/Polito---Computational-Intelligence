import random
from game import Game, Move, Player
from utils import *

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        return random.choice(get_all_valid_moves(game.get_board(), game.get_current_player()))
    
    def __str__(self):
        return 'Random player'