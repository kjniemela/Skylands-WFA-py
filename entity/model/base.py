class Model:
    def __init__(self):
        self.width = 40
        self.height_head = 18
        self.height_body = 48

        self.sneak_height_diff = 12

        # left edge of hitbox rel to entity (x, y)
        self.x_offset = 0