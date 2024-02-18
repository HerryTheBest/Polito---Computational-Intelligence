import random
from game import Game, Move, Player
from utils import *
import numpy


class Gbot(Player):
    def __init__(self):
        super().__init__()
        self.generations = 10
        self.population_size = 20
        self.survivors = int(0.2 * self.population_size)
        self.mutation_rate = 0.5


    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        population = self.generate_population(game)
        fitted_population = list()
        for generation in range(self.generations):
            #fitness
            new_fitted_population = self.fitness(population, game)
            fitted_population += new_fitted_population

            #selection
            fitted_population.sort(key=lambda x: x[1], reverse=True)
            top_population = fitted_population[0 : self.survivors]
            if generation+1 < self.generations: #don't reproduce on the last generation
                #reproduction & mutation
                population = self.reproduction(top_population)

        #select top
        from_pos, move = top_population[0][0]
        return from_pos, move
    

    def generate_population(self, game : Game):
        population = list()
        for _ in range(self.population_size):
            from_pos, move = valid_random_move(game)
            population.append((from_pos, move))
        return population
    

    def fitness(self, population : list(), game : Game):
        fitted_population = list()
        player = game.get_current_player()
        for individual in population:
            #simulate move
            move_result = numpy.array(simulate_move(game.get_board(), player, individual[0], individual[1]))
            fitness_score = 0
            
            #fitness1: promote longer sequences, not necessarely continuous
            for row in move_result:
                fitness_score += numpy.sum(row == player)**2
            for col in move_result.T:
                fitness_score += numpy.sum(col == player)**2
            main_diagonal = move_result.diagonal()
            fitness_score += numpy.sum(main_diagonal == player)**2
            secondary_diagonal = numpy.fliplr(move_result).diagonal()
            fitness_score += numpy.sum(secondary_diagonal == player)**2


            #fitness2: prefer to remove opponent pieces, not own pieces
            if game.get_board()[individual[0][1]][individual[0][0]] == game.get_current_player():
                fitness_score -= 1
            elif game.get_board()[individual[0][1]][individual[0][0]] == (1 - game.get_current_player()):
                fitness_score += 1

            
            fitted_population.append((individual, fitness_score))
        return fitted_population

            
    def reproduction(self, fitted_population):
        offsprings = list()
        functional_offsprings = list()
        num_offsprings = self.population_size - len(fitted_population)

        #crossover
        for _ in range(num_offsprings):
            parent1, parent2 = random.sample(fitted_population, 2)
            offsprings.append((parent1[0][0], parent2[0][1]))
        
        '''
        #mutation
        for offspring in offsprings:
            if random.uniform(0, 1) > self.mutation_rate:
                mutation = random.choice([0, 1, 2])
                if mutation == 0:
                    offspring[0][0] = random.randint(0, 4)
                if mutation == 1:
                    offspring[0][1] = random.randint(0, 4)
                if mutation == 2:
                    offspring[1] = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        '''

        #discard nonfunctional offsprings
        for offspring in offsprings:
            acceptable = True
            if offspring[0][0] == 0 and offspring[1] == Move.LEFT:
                acceptable = False
            if offspring[0][0] == 4 and offspring[1] == Move.RIGHT:
                acceptable = False
            if offspring[0][1] == 0 and offspring[1] == Move.TOP:
                acceptable = False
            if offspring[0][1] == 4 and offspring[1] == Move.BOTTOM:
                acceptable = False
            if acceptable:
                functional_offsprings.append(offspring)


        return functional_offsprings
    
    def __str__(self):
        return 'Gbot'
