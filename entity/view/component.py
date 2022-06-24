from cgitb import text


class Component:
    def __init__(self, texture, offset_left, offset_right, pivot):
        self.texture = texture
        self.offset = {
            -1: offset_left,
            1: offset_right,
        }
        self.pivot = pivot

        self.parent = None
        self.children = []