from cgitb import text


class Component:
    def __init__(self, texture, offset_left, offset_right, pivot):
        self.texture = texture
        self.set_offset(offset_left, offset_right)
        self.set_pivot(pivot)

        self.angle = 0

        self.parent = None

    def set_offset(self, offset_left, offset_right):
        self.offset = {
            -1: offset_left,
            1: offset_right,
        }

    def set_pivot(self, pivot):
        self.pivot = pivot

    def set_angle(self, angle):
        self.angle = angle

    def set_parent(self, parent):
        self.parent = parent

    def get_offset(self, facing):
        if self.parent == None:
            return self.offset[facing]
        else:
            return self.parent.get_offset(facing) + self.offset[facing].rotated(self.parent.get_angle() * facing)

    def get_angle(self):
        if self.parent == None:
            return self.angle
        else:
            return self.parent.get_angle() + self.angle
