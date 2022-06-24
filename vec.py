import math

def Sin(x):
    return math.sin(math.radians(x))

def Cos(x):
    return math.cos(math.radians(x))

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

    def __neg__(self):
        x = -self.x
        y = -self.y

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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def perpendicular(self):
        return Vec(-self.y, self.x)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalized(self):
        try:
            return self / self.magnitude()
        except ZeroDivisionError:
            return self ## TODO - what should this return??

    def rotate(self, theta):
        x, y = self.x, self.y
        self.x = x*Cos(theta) - y*Sin(theta)
        self.y = x*Sin(theta) + y*Cos(theta)

        return self

    def screen_coords(self):
        return (self.x, -self.y)