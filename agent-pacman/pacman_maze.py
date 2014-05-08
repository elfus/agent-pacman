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

class PacmanPoint(pygame.sprite.Sprite):
    """This class represents the bar at the bottom that the player controls """

    def __init__(self, x, y):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a BLUE wall, of the size specified in the parameters
        self.small_dot , self.small_dot_rect = load_image("punto-peque.png")
        self.big_dot , self.big_dot_rect = load_image("punto-gde.png")
        self.image = self.small_dot#pygame.Surface([width, height])
        #self.image.fill(color)

        self.tile_centerx = x
        self.tile_centery = y

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.centery = y # y is the centery
        self.rect.centerx = x # x is the centerx
        # If it's not an energize is assumed to be a normal point
        self.set_energizer(False)

        self.board_tile = 0

    def set_energizer(self, boolean):
        self.is_energizer = boolean
        if boolean == False:
            self.image = self.small_dot
        elif boolean == True:
            self.image = self.big_dot
        self.rect = self.image.get_rect()
        self.rect.centery = self.tile_centery # y is the centery
        self.rect.centerx = self.tile_centerx # x is the centerx

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

            if tile.board_coordinate[0] >= 11 and tile.board_coordinate[0] <= 16 \
                    and tile.board_coordinate[1] >= 16 and tile.board_coordinate[1] <=18:
                    tile.is_in_ghost_house = True

            if tile.board_coordinate == (13,15) or tile.board_coordinate == (14,15):
                tile.is_in_ghost_house = True


            # These are meant to draw on screen the tiles for scatter mode, only that
            if tile.board_coordinate == (0,TILE_HEIGHT_COUNT-1) or tile.board_coordinate == (TILE_WIDTH_COUNT-1,TILE_HEIGHT_COUNT-1):
                tile.is_scatter_tile = True

            if tile.board_coordinate == (3,0) or tile.board_coordinate == (TILE_WIDTH_COUNT-4,0):
                tile.is_scatter_tile = True
    boardMatrix[12][15].is_in_ghost_house = True
    boardMatrix[13][15].is_in_ghost_house = True
    boardMatrix[14][15].is_in_ghost_house = True
    boardMatrix[15][15].is_in_ghost_house = True


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

def generate_pacman_points(boardMatrix):
    POINT_WIDTH = 2
    POINT_HEIGHT = 2
    ENERGIZER_WIDTH = 6
    ENERGIZER_HEIGHT = 6
    pointsGroup = pygame.sprite.Group()
    for row in boardMatrix:
        for tile in row:
            if tile.board_coordinate[1] > 3 and tile.board_coordinate[1] < (TILE_HEIGHT_COUNT-3):
                if tile.board_coordinate[1] > 11 and tile.board_coordinate[1]<23 and tile.board_coordinate[0] > 6 and tile.board_coordinate[0]<21:
                    continue
                if tile.board_coordinate[1] > 11 and tile.board_coordinate[1]<23 and tile.board_coordinate[0] >=0 and tile.board_coordinate[0]<6:
                    continue
                if tile.board_coordinate[1] > 11 and tile.board_coordinate[1]<23 and tile.board_coordinate[0] >21 and tile.board_coordinate[0]<TILE_WIDTH_COUNT:
                    continue
                if tile.is_walkable and not tile.is_in_ghost_house:
                    if tile.board_coordinate == (1,6) or tile.board_coordinate == (TILE_WIDTH_COUNT-2,6) or tile.board_coordinate == (1,26) or tile.board_coordinate == (TILE_WIDTH_COUNT-2,26):
                        point = PacmanPoint(tile.rect.centerx, tile.rect.centery)
                        point.is_energizer = True
                        point.image = point.big_dot
                    else:
                        point = PacmanPoint(tile.rect.centerx, tile.rect.centery)
                    point.board_tile = tile
                    pointsGroup.add(point)
    return pointsGroup