import copy
from random import random, randint, choice
from matplotlib import pyplot as plt

import numpy as np

import constants
import helpers
import random_algorithm
from direction import Direction
from point import Point
from segment import Segment


class GeneticAlgorithm:
    def __init__(self, board):
        self.board_to_solve = board
        self.population = []
        self.population_count = constants.POPULATION_COUNT
        self.tournament_pressure = constants.TOURNAMENT_PRESSURE

    def initialize_population(self):
        ra = random_algorithm.RandomAlgorithm(self.board_to_solve)
        self.population = ra.resolve_paths(self.population_count)

    def tournament_selection(self):
        selection_count = self.tournament_pressure * self.population_count
        random_population = dict()
        while len(random_population) < selection_count:
            index = randint(0, self.population_count - 1)
            random_population[index] = self.population[index]
        min_cost = np.Infinity
        best_candidate = None
        for board in random_population.values():
            if helpers.cost_function(board) < min_cost:
                best_candidate = board
                min_cost = helpers.cost_function(board)
        return best_candidate

    def roulette_wheel_selection(self):
        costs = 0
        weights = []
        for individual in self.population:
            costs += helpers.cost_function(individual)
        population_count = len(self.population)
        for individual in self.population:
            weight = helpers.cost_function(individual)/costs
            weight = 1 - weight
            weight = weight / population_count
            weights.append(weight)

        choose_individual=random()
        index=0
        current_sum=0
        while current_sum<choose_individual and index<population_count-1:
            current_sum+=weights[index]
            index+=1
        print(round(sum(weights)))
        return self.population[index-1]

    def crossover(self, parent1, parent2):
        cross_chance = random()
        new_solution = copy.deepcopy(parent1)
        if cross_chance < constants.CROSS_PROBABILITY:
            for i in range(0, len(new_solution.paths)):
                parent_gen = choice([True, False])
                if not parent_gen:
                    new_solution.paths[i] = parent2.paths[i]
        return new_solution

    def mutation(self, board):
        for i in range(0, len(board.paths)):
            mutation_chance = random()
            if mutation_chance <= constants.MUTATION_PROBABILITY:
                path_to_mutate = board.paths[i]
                mutation_index = randint(0, len(path_to_mutate.segments) - 1)
                previous_segment = path_to_mutate.segments[mutation_index - 1] if mutation_index > 0 else None
                mutating_segment = path_to_mutate.segments[mutation_index]
                next_segment = path_to_mutate.segments[mutation_index + 1] if mutation_index < len(
                    path_to_mutate.segments) - 1 else None
                start_point = self.find_point(path_to_mutate, mutation_index)
                move_direction = choice([-1, 1])
                move_distance = 0
                if mutating_segment.direction == Direction.UP or mutating_segment.direction == Direction.DOWN:
                    if move_direction == 1:
                        if start_point.x == self.board_to_solve.width - 1:
                            move_direction = 0
                        else:
                            move_distance = randint(1, self.board_to_solve.width - 1 - start_point.x)
                    else:
                        if start_point.x == 0:
                            move_direction = 0
                        else:
                            move_distance = randint(1, start_point.x)
                else:
                    if move_direction == 1:
                        if start_point.y + 1 == self.board_to_solve.height:
                            move_direction = 0
                        else:
                            move_distance = randint(1, self.board_to_solve.height - 1 - start_point.y)
                    else:
                        if start_point.y == 0:
                            move_direction = 0
                        else:
                            move_distance = randint(1, start_point.y)
                if next_segment is not None:
                    if next_segment.direction == Direction.UP or next_segment.direction == Direction.RIGHT:
                        next_segment.length -= move_direction * move_distance
                        if next_segment.length < 0:
                            next_segment.length = abs(next_segment.length)
                            if next_segment.direction == Direction.UP:
                                next_segment.direction = Direction.DOWN
                            else:
                                next_segment.direction = Direction.LEFT
                    else:
                        next_segment.length += move_direction * move_distance
                        if next_segment.length < 0:
                            next_segment.length = abs(next_segment.length)
                            if next_segment.direction == Direction.DOWN:
                                next_segment.direction = Direction.UP
                            else:
                                next_segment.direction = Direction.RIGHT
                elif move_direction != 0:
                    if mutating_segment.direction == Direction.UP or mutating_segment.direction == Direction.DOWN:
                        if move_direction == 1:
                            path_to_mutate.segments.append(Segment(Direction.LEFT, move_distance))
                        else:
                            path_to_mutate.segments.append(Segment(Direction.RIGHT, move_distance))
                    else:
                        if move_direction == 1:
                            path_to_mutate.segments.append(Segment(Direction.DOWN, move_distance))
                        else:
                            path_to_mutate.segments.append(Segment(Direction.UP, move_distance))
                if previous_segment is not None:
                    if previous_segment.direction == Direction.UP or previous_segment.direction == Direction.RIGHT:
                        previous_segment.length += move_direction * move_distance
                        if previous_segment.length < 0:
                            previous_segment.length = abs(previous_segment.length)
                            if previous_segment.direction == Direction.UP:
                                previous_segment.direction = Direction.DOWN
                            else:
                                previous_segment.direction = Direction.LEFT
                    else:
                        previous_segment.length -= move_direction * move_distance
                        if previous_segment.length < 0:
                            previous_segment.length = abs(previous_segment.length)
                            if previous_segment.direction == Direction.DOWN:
                                previous_segment.direction = Direction.UP
                            else:
                                previous_segment.direction = Direction.RIGHT
                elif move_direction != 0:
                    if mutating_segment.direction == Direction.UP or mutating_segment.direction == Direction.DOWN:
                        if move_direction == 1:
                            path_to_mutate.segments.insert(0, Segment(Direction.RIGHT, move_distance))
                        else:
                            path_to_mutate.segments.insert(0, Segment(Direction.LEFT, move_distance))
                    else:
                        if move_direction == 1:
                            path_to_mutate.segments.insert(0, Segment(Direction.UP, move_distance))
                        else:
                            path_to_mutate.segments.insert(0, Segment(Direction.DOWN, move_distance))
                self.fix_path(path_to_mutate)
        return board

    def fix_path(self, path):
        to_remove = []
        for i in range(0, len(path.segments)):
            if path.segments[i].length == 0:
                to_remove.append(i)
        to_remove.reverse()
        for i in to_remove:
            del path.segments[i]
        previous_segment = path.segments[0]
        length = len(path.segments)
        i = 1
        while i < length:
            current_segment = path.segments[i]
            if previous_segment.direction == current_segment.direction:
                previous_segment.length += current_segment.length
                del path.segments[i]
                i -= 1
                length -= 1
            if (previous_segment.direction == Direction.UP and current_segment.direction == Direction.DOWN) or (
                    previous_segment.direction == Direction.DOWN and current_segment.direction == Direction.UP) \
                    or (previous_segment.direction == Direction.LEFT and current_segment.direction == Direction.RIGHT) \
                    or (previous_segment.direction == Direction.RIGHT and current_segment.direction == Direction.LEFT):
                if previous_segment.length > current_segment.length:
                    previous_segment.length -= current_segment.length
                    del path.segments[i]
                    i -= 1
                    length -= 1
                elif previous_segment.length < current_segment.length:
                    current_segment.length -= previous_segment.length
                    del path.segments[i - 1]
                    i -= 1
                    length -= 1
                else:
                    del path.segments[i]
                    del path.segments[i - 1]
                    i -= 2
                    length -= 2
            if i < 0:
                i += 1
            previous_segment = path.segments[i]
            i += 1

    def find_point(self, path, segment_index):
        start_point = copy.deepcopy(path.start_point)
        for i in range(0, segment_index):
            if path.segments[i].direction == Direction.UP:
                start_point.y += path.segments[i].length
            elif path.segments[i].direction == Direction.DOWN:
                start_point.y -= path.segments[i].length
            elif path.segments[i].direction == Direction.LEFT:
                start_point.x -= path.segments[i].length
            elif path.segments[i].direction == Direction.RIGHT:
                start_point.x += path.segments[i].length
        return start_point

    def get_best_paths(self):
        self.initialize_population()
        self.roulette_wheel_selection()
        for i in range(0, constants.GENERATION_COUNT):
            new_generation = []
            for j in range(0, self.population_count):
                parent1 = self.tournament_selection()
                parent2 = self.tournament_selection()
                new_individual = self.crossover(parent1, parent2)
                #helpers.plot_board(new_individual,"","")
                self.mutation(new_individual)
                #helpers.plot_board(new_individual,"","")
                new_generation.append(new_individual)

            costs = []
            for individual in new_generation:
                costs.append(helpers.cost_function(individual))
            best_board = new_generation[costs.index(min(costs))]
            print(best_board)
            cost_detail = dict()
            cost_detail["Length"] = helpers.get_length_cost(best_board)
            cost_detail["Segments"] = helpers.get_segment_count_cost(best_board)
            cost_detail["Cross"] = helpers.get_cross_cost(helpers.get_segments_points(best_board))
            self.population = new_generation
            helpers.plot_board(best_board, cost_detail, i)
        plt.show()


'''
    def mutation(self, board):
        for i in range(0, len(board.paths)):
            mutation_chance = random()
            if mutation_chance <= constants.MUTATION_PROBABILITY:
                board.paths[i].segments.clear()
                random_algorithm.resolve_path(board, board.paths[i])
    
        def mutation(self, board):
        for i in range(0, len(board.paths)):
            mutation_chance = random()
            if mutation_chance <= constants.MUTATION_PROBABILITY:
                path_to_mutate = board.paths[i]
                mutation_index = randint(0, len(path_to_mutate.segments) - 1)
                previous_segment = path_to_mutate.segments[mutation_index - 1] if mutation_index > 0 else None
                mutating_segment = path_to_mutate.segments[mutation_index]
                next_segment = path_to_mutate.segments[mutation_index + 1] if mutation_index < len(
                    path_to_mutate.segments) - 1 else None
                start_point = self.find_point(path_to_mutate, mutation_index)
                move_direction = choice([-1, 1])
                move_distance = 0
                if mutating_segment.direction == Direction.UP or mutating_segment.direction == Direction.DOWN:
                    if move_direction == 1:
                        if start_point.x == self.board_to_solve.width - 1:
                            move_direction = 0
                        else:
                            move_distance = randint(1, self.board_to_solve.width - 1 - start_point.x)
                    else:
                        if start_point.x == 0:
                            move_direction = 0
                        else:
                            move_distance = randint(1, start_point.x)
                else:
                    if move_direction == 1:
                        if start_point.y + 1 == self.board_to_solve.height:
                            move_direction = 0
                        else:
                            move_distance = randint(1, self.board_to_solve.height - 1 - start_point.y)
                    else:
                        if start_point.y == 0:
                            move_direction = 0
                        else:
                            move_distance = randint(1, start_point.y)
                if next_segment is not None:
                    if next_segment.direction == Direction.UP or next_segment.direction == Direction.RIGHT:
                        next_segment.length -= move_direction
                    else:
                        next_segment.length += move_direction
                elif move_direction != 0:
                    if mutating_segment.direction == Direction.UP or mutating_segment.direction == Direction.DOWN:
                        if move_direction == 1:
                            path_to_mutate.segments.append(Segment(Direction.LEFT, 1))
                        else:
                            path_to_mutate.segments.append(Segment(Direction.RIGHT, 1))
                    else:
                        if move_direction == 1:
                            path_to_mutate.segments.append(Segment(Direction.DOWN, 1))
                        else:
                            path_to_mutate.segments.append(Segment(Direction.UP, 1))
                if previous_segment is not None:
                    if previous_segment.direction == Direction.UP or previous_segment.direction == Direction.RIGHT:
                        previous_segment.length += move_direction
                    else:
                        previous_segment.length -= move_direction
                elif move_direction != 0:
                    if mutating_segment.direction == Direction.UP or mutating_segment.direction == Direction.DOWN:
                        if move_direction == 1:
                            path_to_mutate.segments.insert(0, Segment(Direction.RIGHT, 1))
                        else:
                            path_to_mutate.segments.insert(0, Segment(Direction.LEFT, 1))
                    else:
                        if move_direction == 1:
                            path_to_mutate.segments.insert(0, Segment(Direction.UP, 1))
                        else:
                            path_to_mutate.segments.insert(0, Segment(Direction.DOWN, 1))
                self.fix_path(path_to_mutate)
        return board


    def fix_path(self, path):
        to_remove = []
        for i in range(0, len(path.segments)):
            if path.segments[i].length == 0:
                to_remove.append(i)
        to_remove.reverse()
        for i in to_remove:
            del path.segments[i]
        previous_segment = path.segments[0]
        length = len(path.segments)
        i = 1
        while i < length:
            current_segment = path.segments[i]
            if previous_segment.direction == current_segment.direction:
                previous_segment.length += current_segment.length
                del path.segments[i]
                i -= 1
                length -= 1
            if (previous_segment.direction == Direction.UP and current_segment.direction == Direction.DOWN) or (
                    previous_segment.direction == Direction.DOWN and current_segment.direction == Direction.UP) \
                    or (previous_segment.direction == Direction.LEFT and current_segment.direction == Direction.RIGHT) \
                    or (previous_segment.direction == Direction.RIGHT and current_segment.direction == Direction.LEFT):
                if previous_segment.length > current_segment.length:
                    previous_segment.length -= current_segment.length
                    del path.segments[i]
                    i -= 1
                    length -= 1
                elif previous_segment.length < current_segment.length:
                    current_segment.length -= previous_segment.length
                    del path.segments[i - 1]
                    i -= 1
                    length -= 1
                else:
                    del path.segments[i]
                    del path.segments[i - 1]
                    i -= 2
                    length -= 2
            if i < 0:
                i += 1
            previous_segment = path.segments[i]
            i += 1
'''
