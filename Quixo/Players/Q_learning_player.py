from collections import namedtuple
from itertools import combinations
import random
import numpy

from copy import deepcopy
from collections import defaultdict
from tqdm.auto import tqdm

from game import Game, Move, Player
from Players.random_player import RandomPlayer
from utils import *


class Qbot(Player):
    def __init__(self, training_epochs, role, exploration_logic=RandomPlayer(), training_opponent=RandomPlayer(), 
                 learning_rate=0.9, discount_factor=0.9, exploration_rate=0.1):
        super().__init__()
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.learning_dictionary = defaultdict(int)
        self.game_log = list()
        self.training_epochs = training_epochs
        self.role = role
        self.exploration_logic = exploration_logic
        self.training_opponent = training_opponent
        self.training = True
        self.unencountered_states = 0

        self.train(training_epochs)


    def train(self, epochs : int):
        print(f'Training Qbot over {epochs} epochs')
        for _ in tqdm(range(epochs)):
            g = Game()
            if self.role == 0:
                winner = g.play(self, self.training_opponent)
            elif self.role == 1:
                winner = g.play(self.training_opponent, self)
            self.update(winner)
        
        self.training = False
        self.exploration_rate = 0


    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        hashable_state = tuple(map(tuple, game.get_board()))

        if random.uniform(0, 1) > self.exploration_rate and self.learning_dictionary[hashable_state] != 0:
            # exploit, aka choose a move based on what it has learned so far
            moves, rewards = self.learning_dictionary[hashable_state] # get a list of possible moves from the current state
            best_move_index = rewards.index(max(rewards))
            if max(rewards) > 0:
                from_pos, move = moves[best_move_index]
            else:
                #no memorized option has lead to victory, explore a new one
                from_pos, move = self.exploration_logic.make_move(game)
        else:
            # explore, aka make a new random move outside of what it has learned so far
            from_pos, move = self.exploration_logic.make_move(game)
            if not self.train:
                self.unencountered_states += 1
                print(self.unencountered_states)

        if self.training:
            self.game_log.append((deepcopy(game.get_board()), (from_pos, move)))
        return from_pos, move


    def update(self, victory):
        reward = 1 if (victory == self.role) else -1

        for board, move in self.game_log: # for each move taken during the game
            hashable_state = tuple(map(tuple, board))
            
            existing_state = self.learning_dictionary[hashable_state]
            if existing_state == 0:
                self.learning_dictionary[hashable_state] = [[], []]

            previous_moves: list = self.learning_dictionary[hashable_state][0]
            if move in previous_moves:
                i = previous_moves.index(move)
                current_reward = self.learning_dictionary[hashable_state][1][i]
                optimal_next_reward = 0
                
                #get the board state after this move
                next_opponent_board = simulate_move(board, self.role, move[0], move[1])
                #simulate all possible moves the opponent might make
                for opponent_move in get_all_valid_moves(next_opponent_board, (1 - self.role)):
                    next_board = simulate_move(next_opponent_board, (self.role - 1), opponent_move[0], opponent_move[1])
                    hashable_next_state = tuple(map(tuple, next_board))
                    if self.learning_dictionary[hashable_next_state] != 0:
                        if max(self.learning_dictionary[hashable_next_state][1]) > optimal_next_reward:
                            optimal_next_reward = max(self.learning_dictionary[hashable_next_state][1])

                # self.learning_dictionary[hashable_state][1][i] = previous_reward * self.learning_rate + (reward - previous_reward) * self.discount_factor
                self.learning_dictionary[hashable_state][1][i] = current_reward * (1 - self.learning_rate) + self.learning_rate * (reward + self.discount_factor * optimal_next_reward)
            else:
                move_reward = reward * self.discount_factor
                self.learning_dictionary[hashable_state][0].append(move)
                self.learning_dictionary[hashable_state][1].append(move_reward)
        
        self.game_log = list()


    def __str__(self):
        return f'Qbot, trained over {self.training_epochs} games with {self.exploration_logic} logic'