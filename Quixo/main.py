import random
from game import Game, Move, Player
from Players.random_player import RandomPlayer
from Players.Q_learning_player import Qbot
from Players.genetic_player import Gbot
from Players.Simple_player import SimpleBot
from tqdm import tqdm


def play(player1, player2, rounds, show=False):
    score = [0, 0, 0]
    for _ in tqdm(range(rounds)):
        g = Game()
        winner = g.play(player1, player2)
        score[winner] += 1
        if show:
            g.print()
            print(f"Winner: Player {winner}")
    print('-------------------------------------------------------------------------------------')
    print(f'### After {rounds} games: [{player1}] won {score[0]}, [{player2}] won {score[1]} ###')
    print('-------------------------------------------------------------------------------------')
    

if __name__ == '__main__':
    #player1 = Qbot(10_000, 0, SimpleBot())
    #player1 = Qbot(10_000, 0)
    
    player2 = RandomPlayer()

    player3 = Gbot()

    player4 = SimpleBot()

    #playing
    n_games = 1_000
    print(f'Playing {n_games} games')
    play(player4, player2, n_games)
