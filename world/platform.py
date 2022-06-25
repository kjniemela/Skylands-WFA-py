from utils import *
from config import config

class Surface:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.line = (p, q)
        self.dst = (q - p)
        self.normal = self.dst.perpendicular().normalized()

        if self.normal @ Vec(0, 1) >= 1 - math.sin(math.radians(0.25)):
            self.normal = Vec(0, 1)

        if config["debug"] and config["verbose"]:
            print("Surface(%s, dst=%s, normal=%s)" % (self.line, self.dst, self.normal))


class Platform:
    def __init__(self, texture, pos, w, h, d, pivot):
        self.texture = texture
        self.center = pos
        self.pivot = pivot
        self.top_left = pos - Vec(w / 2, -h / 2)
        self.w, self.h, self.d = w, h, d

    def get_verts(self, camX, camY, b=1):
        x1 = self.x - ((self.w/2) * Cos(-self.d)*b) + ((self.h/2) * Sin(-self.d)*b)
        y1 = self.y + ((self.h/2) * Cos(-self.d)*b) + ((self.w/2) * Sin(-self.d)*b)
        x2 = self.x + ((self.w/2) * Cos(-self.d)*b) + ((self.h/2) * Sin(-self.d)*b)
        y2 = self.y + ((self.h/2) * Cos(-self.d)*b) - ((self.w/2) * Sin(-self.d)*b)

        x3 = self.x - ((self.w/2) * Cos(-self.d)*b) - ((self.h/2) * Sin(-self.d))
        y3 = self.y - ((self.h/2) * Cos(-self.d)*b) + ((self.w/2) * Sin(-self.d))
        x4 = self.x + ((self.w/2) * Cos(-self.d)*b) - ((self.h/2) * Sin(-self.d))
        y4 = self.y - ((self.h/2) * Cos(-self.d)*b) - ((self.w/2) * Sin(-self.d))

        return [
            (x1, y1),
            (x2, y2),
            (x3, y3),
            (x4, y4)
            ]
