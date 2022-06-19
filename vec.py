from utils import distance

class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "%s / %s" % (self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y

        return Vec(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y

        return Vec(x, y)

    def __truediv__(self, m):
        x = self.x / m
        y = self.y / m

        return Vec(x, y)

    def __iter__(self):
        for e in (self.x, self.y):
            yield e

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError

    def perpendicular(self):
        return Vec(self.y, self.x)

    def magnitude(self):
        return distance(0, 0, self.x, self.y)

    def normalized(self):
        return self / self.magnitude()

    def screen_coords(self):
        return (self.x, -self.y)