from cgitb import text


class Component:
    def __init__(self, texture, offset_left, offset_right, pivot):
        self.texture = texture
        self.set_offset(offset_left, offset_right)
        self.set_pivot(pivot)

        self.parent = None

    def set_offset(self, offset_left, offset_right):
        self.offset = {
            -1: offset_left,
            1: offset_right,
        }

    def set_pivot(self, pivot):
        self.pivot = pivot

    def get_offset(self, facing):
        if self.parent == None:
            return self.offset[facing]
