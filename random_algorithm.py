import copy
import random

import numpy as np

import helpers
from direction import Direction
from segment import Segment


def get_direction(axis, current_point, end_point, board_width, board_height):
    if axis:
        if current_point.x == 0:
            return Direction.RIGHT
        elif current_point.x == board_width - 1:
            return Direction.LEFT
        else:
            return Direction.RIGHT if current_point.x < end_point.x else Direction.LEFT if current_point.x > end_point.x else \
                random.choice([Direction.LEFT, Direction.RIGHT])
    else:
        if current_point.y == 0:
            return Direction.UP
        elif current_point.y == board_height - 1:
            return Direction.DOWN
        else:
            return Direction.UP if current_point.y < end_point.y else Direction.DOWN if current_point.y > end_point.y else \
                random.choice([Direction.UP, Direction.DOWN])


def get_segment_length(current_point, direction, board, end_point):
    if direction == Direction.UP or direction == Direction.DOWN:
        max_length = abs(current_point.y - end_point.y)
        if max_length == 0:
            if direction == Direction.UP:
                max_length = board.height - current_point.y - 1
            else:
                max_length = current_point.y
    else:
        max_length = abs(current_point.x - end_point.x)
        if max_length == 0:
            if direction == Direction.RIGHT:
                max_length = board.width - current_point.x - 1
            else:
                max_length = current_point.x
    return random.randint(1, max_length)


def resolve_path(board, path):
    current_point = copy.deepcopy(path.start_point)
    axis = random.choice([True, False])
    while not current_point.__eq__(path.end_point):
        direction = get_direction(axis, current_point, path.end_point, board.width, board.height)
        segment_length = get_segment_length(current_point, direction, board, path.end_point)
        path.segments.append(Segment(direction, segment_length))
        if direction == Direction.UP:
            current_point.y += segment_length
        elif direction == Direction.DOWN:
            current_point.y -= segment_length
        elif direction == Direction.LEFT:
            current_point.x -= segment_length
        elif direction == Direction.RIGHT:
            current_point.x += segment_length
        axis = not axis


class RandomAlgorithm:
    def __init__(self, board):
        self.board = board

    def resolve_paths(self, n):
        resolved_boards = []
        for i in range(0, n):
            new_board = copy.deepcopy(self.board)
            for path in new_board.paths:
                path.segments.clear()
                resolve_path(new_board, path)
            resolved_boards.append(new_board)
        return resolved_boards

    def get_best_paths(self, n):
        boards = self.resolve_paths(n)
        costs = []
        for board in boards:
            costs.append(helpers.cost_function(board))
        print('Best: {}, Worst: {}, Avg: {}, Std: {}'.format(min(costs), max(costs), np.average(costs), np.std(np.array(costs))))
        best_board = boards[costs.index(min(costs))]
        cost_detail = dict()
        cost_detail["Length"] = helpers.get_length_cost(best_board)
        cost_detail["Segments"] = helpers.get_segment_count_cost(best_board)
        cost_detail["Cross"] = helpers.get_cross_cost(helpers.get_segments_points(best_board))
        return best_board, cost_detail
