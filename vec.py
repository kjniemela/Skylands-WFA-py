import math

class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vec(%s, %s)" % (self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y

        return Vec(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y

        return Vec(x, y)

    def __mul__(self, other):
        if type(other) == Vec:
            pass
        else:
            return Vec(self.x * other, self.y * other)

    def __matmul__(self, other):
        return self.x * other.x + self.y * other.y

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
        return Vec(-self.y, self.x)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalized(self):
        try:
            return self / self.magnitude()
        except ZeroDivisionError:
            return self ## TODO - what should this return??

    def screen_coords(self):
        return (self.x, -self.y)