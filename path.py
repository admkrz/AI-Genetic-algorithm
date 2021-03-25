from direction import Direction
from point import Point


class Path:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.segments = []

    def get_points(self):
        points=[self.start_point]
        for segment in self.segments:
            for i in range(0, segment.length):
                if segment.direction == Direction.UP:
                    points.append(Point(points[-1].x, points[-1].y + 1))
                elif segment.direction == Direction.DOWN:
                    points.append(Point(points[-1].x, points[-1].y - 1))
                elif segment.direction == Direction.LEFT:
                    points.append(Point(points[-1].x - 1, points[-1].y))
                elif segment.direction == Direction.RIGHT:
                    points.append(Point(points[-1].x + 1, points[-1].y))
        return points

    def __str__(self):
        if len(self.segments) == 0:
            return "Path: " + self.start_point.__str__() + "->" + self.end_point.__str__() + "; No Segments"
        else:
            return "Path: " + self.start_point.__str__() + "->" + '->'.join(
                [segment.__str__() for segment in self.segments]) + "->" + self.end_point.__str__()
