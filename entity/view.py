from utils import *
from window import controller

class View:
    def __init__(self):
        self.walk_frame = 0
        self.facing = 1

        # rotation of entity's arms
        self.right_arm = 0
        self.left_arm = 0
        self.right_hand = 0
        self.left_hand = 0

        # position of item held by entity
        self.held_x = 0
        self.held_y = 0