import constants
from matplotlib import pyplot as plt

from direction import Direction


def cost_function(board):
    paths_points = get_segments_points(board)
    length_cost = get_length_cost(board) * constants.PATH_LENGTH_PENALTY
    segment_count_cost = get_segment_count_cost(board) * constants.SEGMENT_COUNT_PENALTY
    cross_cost = get_cross_cost(paths_points) * constants.CROSS_PENALTY
    return length_cost + segment_count_cost + cross_cost


def get_segments_points(board):
    paths_points = []
    for path in board.paths:
        paths_points.append(path.get_points())
    return paths_points


def get_length_cost(board):
    cost = 0
    for path in board.paths:
        for segment in path.segments:
            cost += segment.length
    return cost


def get_segment_count_cost(board):
    cost = 0
    for path in board.paths:
        cost += len(path.segments)
    return cost


def get_cross_cost(paths_points):
    unique_points = dict()
    for path_points in paths_points:
        for point in path_points:
            unique_points[(point.x,point.y)] = 1

    all_points = 0
    for path in paths_points:
        all_points += len(path)

    return all_points - len(unique_points)


def plot_board(board, cost_details, population_number):
    plt.clf()
    for i in range(0, board.width):
        for j in range(0, board.height):
            plt.plot([i], j, 'ro', markersize=2)
    for path in board.paths:
        xs = [path.start_point.x]
        ys = [path.start_point.y]
        last_point = (path.start_point.x, path.start_point.y)
        for segment in path.segments:
            if segment.direction == Direction.UP:
                last_point = (last_point[0], last_point[1] + segment.length)
            elif segment.direction == Direction.DOWN:
                last_point = (last_point[0], last_point[1] - segment.length)
            elif segment.direction == Direction.LEFT:
                last_point = (last_point[0] - segment.length, last_point[1])
            elif segment.direction == Direction.RIGHT:
                last_point = (last_point[0] + segment.length, last_point[1])
            xs.append(last_point[0])
            ys.append(last_point[1])
        plt.plot(xs, ys, linewidth=3, marker='o')
    plt.text(1, 1.06, cost_details, bbox={'facecolor': 'w', 'pad': 5},
             ha="right", va="top", transform=plt.gca().transAxes)
    plt.text(0.2, 1.06, "Generation nr: "+str(population_number), bbox={'facecolor': 'w', 'pad': 5},
             ha="right", va="top", transform=plt.gca().transAxes)
    plt.show(block=False)
    plt.pause(0.01)
