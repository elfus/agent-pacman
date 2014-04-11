__author__ = 'aortegag'

import os
import pygame
from pygame.locals import *

OFFSET = 1
GO_LEFT = [-OFFSET, 0]
GO_RIGHT = [OFFSET, 0]
GO_DOWN = [0, OFFSET]
GO_UP = [0, -OFFSET]
STAND_STILL = [0, 0]

BLACK  = (   0,   0,   0)
WHITE  = ( 255, 255, 255)
BLUE   = (   0,   0, 255)
GREEN  = (   0, 255,   0)
RED    = ( 255,   0,   0)
PURPLE = ( 255,   0, 255)

TILE_WIDTH = 8
TILE_HEIGHT = 8
BOARD_WIDTH = 224
BOARD_HEIGHT = 288
TILE_WIDTH_COUNT = BOARD_WIDTH/TILE_WIDTH
TILE_HEIGHT_COUNT = BOARD_HEIGHT/TILE_HEIGHT

class Tile:
    """Tile representing a tile on the board. It wraps a rect"""
    def __init__(self, left, top, width, height):
        self.rect = Rect(left, top, width, height)
        self.is_walkable = False
        self.is_intersection = False
        self.is_special_intersection = False
        self.board_coordinate = (0,0)

    def setWalkable(self, isWakable):
        self.is_walkable = isWakable

    def getCenter(self):
        return self.rect.center

    def isWalkable(self):
        return self.is_walkable

def load_image(name):
    """ Load image and return image object"""
    fullname = os.path.join('res', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image, image.get_rect()