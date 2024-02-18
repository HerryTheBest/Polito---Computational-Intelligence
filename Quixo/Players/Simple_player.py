import random
from game import Game, Move, Player
from utils import *
import numpy


class SimpleBot(Player):
    def __init__(self):
        super().__init__()


    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        valid_moves = get_all_valid_moves(game.get_board(), game.get_current_player())
        from_pos, move = self.move_fitness(valid_moves, game)
        return from_pos, move
    

    def move_fitness(self, population : list(), game : Game):
        fitted_population = list()
        player = game.get_current_player()
        adversary = 1 - player
        for individual in population:
            #simulate move
            move_result = numpy.array(simulate_move(game.get_board(), player, individual[0], individual[1]))
            fitness_score = 0
            lines = [row for row in move_result]
            lines += [col for col in move_result.T]
            lines += [move_result.diagonal(), numpy.fliplr(move_result).diagonal()]

            #fitness1: promote longer sequences, not necessarely continuous
            for line in lines:
                fitness_score += numpy.sum(line == player)**2


            #fitness2: prefer to remove opponent pieces, not own pieces
            if game.get_board()[individual[0][1]][individual[0][0]] == game.get_current_player():
                fitness_score -= 1
            elif game.get_board()[individual[0][1]][individual[0][0]] == (1 - game.get_current_player()):
                fitness_score += 1

            #fitness3: don't make a move that makes the adversary win
            losing_move = False
            for line in lines:
                if numpy.sum(line == adversary) == 5:
                    losing_move = True
            if losing_move:
                fitness_score -= 1000
            
            fitted_population.append((individual, fitness_score))

        fitted_population.sort(key=lambda x: x[1], reverse=True)
        top_score = fitted_population[0][1]
        top_fitted_population = []
        for individual in fitted_population:
            if individual[1] == top_score:
                top_fitted_population.append(individual)
        return random.choice(top_fitted_population)[0]
        #return fitted_population[0][0]
    
    def __str__(self):
        return 'Simplebot'