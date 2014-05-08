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
        self.is_in_ghost_house = False
        self.is_scatter_tile = False
        self.point_exists = False
        self.visited = False

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

def get_tile_neighbors(boardMatrix, tile):
    """
    Gets the north, south, west and east neighbors from the tile. This function returns neighbors that are walkable
    :param boardMatrix:
    :param tile:
    :return:
    """
    up = (tile.board_coordinate[0],tile.board_coordinate[1]-1)
    down = (tile.board_coordinate[0],tile.board_coordinate[1]+1)
    left = (tile.board_coordinate[0]-1,tile.board_coordinate[1])
    right = (tile.board_coordinate[0]+1,tile.board_coordinate[1])
    m_list = []
    if up[0]>=0 and up[0]<TILE_WIDTH_COUNT and up[1]>=3 and up[1]<TILE_HEIGHT_COUNT-3:
        if (up[0] <= 10 or up[0]>=18) or (up[1] < 15 or up[1] >18):
            tile = boardMatrix[up[0]][up[1]]
            if tile.is_walkable == True:
                m_list.append(tile)
    if down[0]>=0 and down[0]<TILE_WIDTH_COUNT and down[1]>=3 and down[1]<TILE_HEIGHT_COUNT-3:
        if (down[0] <= 10 or down[0]>=18) or (down[1] < 15 or down[1] >18):
            tile = boardMatrix[down[0]][down[1]]
            if tile.is_walkable == True:
                m_list.append(tile)
    if left[0]>=0 and left[0]<TILE_WIDTH_COUNT and left[1]>=3 and left[1]<TILE_HEIGHT_COUNT-3:
        if (left[0] <= 10 or left[0]>=18) or (left[1] < 15 or left[1] >18):
            tile = boardMatrix[left[0]][left[1]]
            if tile.is_walkable == True:
                m_list.append(tile)
    if right[0]>=0 and right[0]<TILE_WIDTH_COUNT and right[1]>=3 and right[1]<TILE_HEIGHT_COUNT-3:
        if (right[0] <= 10 or right[0]>=18) or (right[1] < 15 or right[1] >18):
            tile = boardMatrix[right[0]][right[1]]
            if tile.is_walkable == True:
                m_list.append(tile)

    return m_list