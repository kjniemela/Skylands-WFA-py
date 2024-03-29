import os
import sys
import math
from time import time
from random import randint

from vec import Vec, Sin, Cos

if sys.version_info[0] == 2:
    print("Fatal Error: Skylands WFA is not compatible with python %i.%i.%i. Please use python 3." % (
        sys.version_info[0],
        sys.version_info[1],
        sys.version_info[2],
    ))
    raw_input("Press ENTER to exit.")
    sys.exit()

try:
    import pygame
except ModuleNotFoundError:
    print("ModuleNotFoundError: Pygame module could not be found.")
    if input("Install pygame [Y/n]? ").lower() == "y":
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        import pygame
    else:
        exit()

## Custom Events
MUSIC_END = pygame.event.custom_type()

def resource_path(relative_path):
    """ Ge absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def blitRotateCenter(surf, image, angle, pos, camPos):

    raise Exception("YOU SHOULD NOT BE USING blitRotateCenter! Use blitRotateAround!")

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect().center)

    surf.blit(rotated_image, (new_rect.topleft[0] + pos[0] - camPos[0], new_rect.topleft[1] + pos[1] + camPos[1]))

def blitRotateAround(surf, image, angle, pos, camera_pos, pivot):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = (-pivot).rotate(angle).screen_coords())

    surf.blit(rotated_image, (new_rect.topleft[0] + pos.x - camera_pos.x, new_rect.topleft[1] - pos.y + camera_pos.y))

def screen_coords(point, camX, camY):
    return (point[0]-camX, -(point[1]-camY))

#screen coord transformations
def extend_line_up(x1, y1, x2, y2, y):
    if y1 < y2:
        s = (x1-x2)/(y1-y2)
        return (x1+((y-y1)*s), y, x2, y2)
    else:
        s = (x2-x1)/(y2-y1)
        return (x1, y, x2+((y-y2)*s), y2)

def extend_line_down(x1, y1, x2, y2, y):
    if y1 > y2:
        s = (x1-x2)/(y2-y1)
        return (x1+((y-y1)*s), y, x2, y2)
    else:
        s = (x2-x1)/(y1-y2)
        return (x1, y, x2+((y-y2)*s), y2)

def line_collision(line1, line2, seg=True):
    """
    line1 = (p1: Vec, p2: Vec)
    line2 = (p3: Vec, p4: Vec)
    """
    (x1, y1), (x2, y2) = line1
    (x3, y3), (x4, y4) = line2

    try:
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    except ZeroDivisionError:
        return (False, None)

    if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1) or not seg:
        intersection_x = x1 + (uA * (x2-x1))
        intersection_y = y1 + (uA * (y2-y1))
        return (True, Vec(intersection_x, intersection_y))
    else:
        return (False, None)