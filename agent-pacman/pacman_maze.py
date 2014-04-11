__author__ = 'aortegag'

import pygame
from util import *
from pygame.locals import *

class Wall(pygame.sprite.Sprite):
    """This class represents the bar at the bottom that the player controls """

    def __init__(self, x, y, width, height, color):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a BLUE wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

def create_board_matrix(width, height):
    global BOARD_WIDTH
    global BOARD_HEIGHT
    if width != BOARD_WIDTH or height != BOARD_HEIGHT:
        print "The board has the wrong size"
        return 0

    board_matrix = []
    i, j = 0, 0
    while i < BOARD_WIDTH:
        board_matrix.append([])
        while j < BOARD_HEIGHT:
            row = board_matrix[-1] # get the last row
            new_tile = Tile(i, j, TILE_WIDTH, TILE_HEIGHT)
            new_tile.setWalkable(True)
            row.append(new_tile)
            j += TILE_HEIGHT
        i += TILE_WIDTH
        j = 0

    # This two while loops assign their Tile coordinate
    i, j = 0, 0
    while i < TILE_WIDTH_COUNT:
        board_matrix.append([])
        while j < TILE_HEIGHT_COUNT:
            tile = board_matrix[i][j]
            tile.board_coordinate = (i,j)
            j += 1
        i += 1
        j = 0

    return board_matrix

def detect_walkable_tiles(boardMatrix, wallList):
    for row in boardMatrix:
        for item in row:
            hit = pygame.sprite.spritecollide(item, wallList, False)
            if len(hit) > 0:
                item.setWalkable(False)


def detect_intersections(boardMatrix):
    for row in boardMatrix:
        for tile in row:
            neighbors = get_tile_neighbors(boardMatrix, tile)
            if len(neighbors) >= 3:
                tile.is_intersection = True
                if tile.board_coordinate == (12,14):
                    tile.is_special_intersection = True
                if tile.board_coordinate == (15,14):
                    tile.is_special_intersection = True
                if tile.board_coordinate == (12,26):
                    tile.is_special_intersection = True
                if tile.board_coordinate == (15,26):
                    tile.is_special_intersection = True


def create_wall(maze, x, y):
    width = 0
    height = 0
    MAX_X, MAX_Y = maze.get_size()
    CURRENT_COLOR = maze.get_at([x,y])

    for m_x in range(x,MAX_X):
        color = maze.get_at([m_x,y])
        if CURRENT_COLOR != color or m_x == MAX_X-1:
            width = m_x - x
            if m_x == MAX_X-1:
                width += 1
            break

    for m_y in range(y,MAX_Y):
        color = maze.get_at([x,m_y])
        if CURRENT_COLOR != color:
            height = m_y - y
            break

    return Wall(x,y,width,height, GREEN), x+width


def analyze_maze():
    maze, mazeRect = load_image("grid.bmp")
    width, height = maze.get_size()
    wallSpriteGroup =  pygame.sprite.Group()
    pointsSpriteGroup =  pygame.sprite.Group()

    blackColor = pygame.Color("black")
    redColor = pygame.Color("red")
    whiteColor = pygame.Color("white")

    h = 0
    w = 0
    while h < height:
        w = 0
        while w < width:
            color = maze.get_at([w,h])
            if blackColor != color:
                wall, w = create_wall(maze,w,h)
                w -= 1

                if color == pygame.Color("blue"):
                    if len(pygame.sprite.spritecollide(wall,pointsSpriteGroup,False)) == 0:
                        pointsSpriteGroup.add(wall)
                else:
                    if len(pygame.sprite.spritecollide(wall,wallSpriteGroup,False)) == 0:
                        wallSpriteGroup.add(wall)
            w += 1
        h += 1

    print "Number of rectangles ", len(wallSpriteGroup.sprites())
    print "Number of points ", len(pointsSpriteGroup.sprites())
    return wallSpriteGroup, pointsSpriteGroup