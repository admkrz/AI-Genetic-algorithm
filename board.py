from path import Path
from point import Point


class Board:
    def __init__(self, height, width, paths_coordinates):
        self.width = width
        self.height = height
        self.points = []
        self.paths = []
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.points.append(Point(x, y))
        for path in paths_coordinates:
            self.paths.append(Path(Point(path[0][0], path[0][1]), Point(path[1][0], path[1][1])))

    def __str__(self) -> str:
        return "Board: " + str(self.width) + "x" + str(self.height) + ", Paths to find: \n" + '\n'.join([path.__str__() for path in self.paths])
