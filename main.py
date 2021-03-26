import os
from copy import deepcopy

from matplotlib import pyplot as plt
import constants
import helpers
import random_algorithm
from board import Board
from genetic_algorithm import GeneticAlgorithm
from random_algorithm import RandomAlgorithm


def loadData(filename):
    file = open(filename, "r")
    board_size = file.readline()
    board_size_array = board_size.replace('\n', '').split(';')
    board_size_array = [int(i) for i in board_size_array]
    points_coordinates_strings = file.readlines()
    points_coordinates_strings = [coordinates.replace('\n', '').split(';') for coordinates in
                                  points_coordinates_strings]
    paths_coordinates = []
    counter = 0
    for path in points_coordinates_strings:
        segment = []
        segment_point = []
        for i in path:
            counter += 1
            segment_point.append(int(i))
            if counter % 2 == 0:
                segment.append(segment_point)
                segment_point = []
        paths_coordinates.append(segment)
    return board_size_array, paths_coordinates


def create_board(board_size, paths_coordinates):
    board = Board(board_size[1], board_size[0], paths_coordinates)
    return board


def run():
    filename = ""
    while not os.path.isfile(filename):
        filename = input("Podaj nazwe pliku do wczytania danych\n")
        if not os.path.isfile(filename):
            print("----------------\nPlik nie istnieje\n----------------")
    board_size, paths_coordinates = loadData(filename)
    board = create_board(board_size, paths_coordinates)
    print(board)

    random_algorithm = RandomAlgorithm(board)
    print("-----------------------------------------------")
    n = int(input("Podaj liczbe powtorzen algorytmu losowego:\n"))
    best_paths, cost = random_algorithm.get_best_paths(n)
    print("-----------------------------------------------")
    print(best_paths)
    print("Cost: " + str(cost))
    helpers.plot_board(best_paths, cost, "Random")
    plt.show()

    ra = RandomAlgorithm(board)
    '''
    population = ra.resolve_paths(constants.POPULATION_COUNT)
    constants.POPULATION_COUNT = 50
    genetic_algorithm = GeneticAlgorithm(deepcopy(board), filename, deepcopy(population))
    genetic_algorithm.get_best_paths()
    constants.POPULATION_COUNT = 100
    population = ra.resolve_paths(constants.POPULATION_COUNT)
    genetic_algorithm = GeneticAlgorithm(deepcopy(board), filename, deepcopy(population))
    genetic_algorithm.get_best_paths()
    constants.POPULATION_COUNT = 150
    population = ra.resolve_paths(constants.POPULATION_COUNT)
    genetic_algorithm = GeneticAlgorithm(deepcopy(board), filename, deepcopy(population))
    genetic_algorithm.get_best_paths()
    population = ra.resolve_paths(constants.POPULATION_COUNT)

    genetic_algorithm = GeneticAlgorithm(deepcopy(board), filename, deepcopy(population))
    genetic_algorithm.get_best_paths()
    constants.GENERATION_COUNT = 20
    genetic_algorithm = GeneticAlgorithm(deepcopy(board), filename, deepcopy(population))
    genetic_algorithm.get_best_paths()
    constants.GENERATION_COUNT = 50
    genetic_algorithm = GeneticAlgorithm(deepcopy(board), filename, deepcopy(population))
    genetic_algorithm.get_best_paths()
    constants.GENERATION_COUNT = 100
    genetic_algorithm = GeneticAlgorithm(deepcopy(board), filename, deepcopy(population))
    genetic_algorithm.get_best_paths()
    constants.GENERATION_COUNT = 200
    genetic_algorithm = GeneticAlgorithm(deepcopy(board), filename, deepcopy(population))
    genetic_algorithm.get_best_paths()'''


if __name__ == '__main__':
    run()
