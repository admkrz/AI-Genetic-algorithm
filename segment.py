class Segment:
    def __init__(self, direction, length):
        self.direction = direction
        self.length = length

    def __str__(self) -> str:
        return "(" + self.direction.name.__str__() + ";" + str(self.length) + ")"
