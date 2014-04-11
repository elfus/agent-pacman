from math import sqrt

__author__ = 'aortegag'

import pygame
from pygame.locals import *
from pygame.locals import *
from util import *

WALL_LIST = 0
POINTS_LIST = 0

PACMAN_START = (105,206)
GHOST_START = (105,133)
BLINKY_START = (105, 108)

PACMAN = 0

INDEX_UP = 0
INDEX_RIGHT = 1
INDEX_DOWN = 2
INDEX_LEFT = 3

# OFFSET defined in util.py
DIRECTION_UP = [0, -OFFSET]
DIRECTION_RIGHT = [OFFSET, 0]
DIRECTION_DOWN = [0, OFFSET]
DIRECTION_LEFT = [-OFFSET, 0]

FACING_LEFT = "left"
FACING_RIGHT = "right"
FACING_UP = "up"
FACING_DOWN = "down"

class Character(pygame.sprite.Sprite):
    """A Ghost that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""
    PACMAN = 0

    def __init__(self, FILENAME, boardMatrix):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(FILENAME)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.stop()
        self.name = "Character"
        self.facing = FACING_LEFT
        self.tile_xy = (0,0)
        self.current_tile = 0
        self.board_matrix = boardMatrix
        print 'Character Constructor'

    def stop(self):
        self.movepos = [0, 0]
        self.state = "still"

    def get_direction(self, facing_to):
        if facing_to == FACING_LEFT: return GO_LEFT
        if facing_to == FACING_RIGHT: return GO_RIGHT
        if facing_to == FACING_DOWN: return GO_DOWN
        if facing_to == FACING_UP: return GO_UP

    def get_facing(self, direction):
        if direction == GO_LEFT: return FACING_LEFT
        if direction == GO_RIGHT: return FACING_RIGHT
        if direction == GO_DOWN: return FACING_DOWN
        if direction == GO_UP: return FACING_UP

    def detect_tunnel_condition(self):
        # This is if is meant to detect the case in which any character goes through
        # the 'middle tunnel' on the maze and appears on the other side
        if self.area.contains(self.rect) == False:
            if self.rect.left < (self.area.left - self.rect.width):
                self.rect.left = self.area.right
                return
            if self.rect.right > (self.area.right + self.rect.width):
                self.rect.right = self.area.left
                return

    def update(self):
        self.detect_tunnel_condition()

    def get_adjacent_tile(self, facing_to):
        """
        Gets the adjacent tile to this character depending on where it is facing.
        This variable assumes the attribute variable self.facing is set before
        calling this method.

        :rtype : The tile (Rect) object adjacent where the character is facing
        :return: The tile coordinates in the board matrix
        """
        adjacent_tile = 0
        target_tile = (-1,-1)

        if facing_to == FACING_LEFT:
            target_tile = (self.tile_xy[0]-1,self.tile_xy[1])
        elif facing_to == FACING_RIGHT:
            target_tile = (self.tile_xy[0]+1,self.tile_xy[1])
        elif facing_to == FACING_UP:
            target_tile = (self.tile_xy[0],self.tile_xy[1]-1)
        elif facing_to == FACING_DOWN:
            target_tile = (self.tile_xy[0],self.tile_xy[1]+1)

        if target_tile[0] >= TILE_WIDTH_COUNT:
            target_tile = (0,target_tile[1])

        if target_tile[0] < 0:
            target_tile = (TILE_WIDTH_COUNT-1,target_tile[1])

        if target_tile[1] >= TILE_HEIGHT_COUNT:
            target_tile = (target_tile[0], 0)

        adjacent_tile = self.board_matrix[target_tile[0]][target_tile[1]]
        if adjacent_tile.isWalkable() == False:
            print self.name,": the tile facing",facing_to,"is NOT walkable"
            if facing_to == FACING_LEFT or facing_to == FACING_RIGHT:
                if self.current_tile.rect.centerx != self.rect.centerx:
                    adjacent_tile = self.current_tile
                    target_tile = self.tile_xy
            elif facing_to == FACING_UP or facing_to == FACING_DOWN:
                if self.current_tile.rect.centery != self.rect.centery:
                    adjacent_tile = self.current_tile
                    target_tile = self.tile_xy

        return adjacent_tile, target_tile

    def movedirection(self, direction, pointsGroup):
        """

        :param direction: The direction the Character should go
        :param pointsGroup: A list of all the points that pacman can eat
        :return: True when the Character was able to move to the given direction, False otherwise
        """
        if self.can_move_to(direction) == False:
            return False

        new_facing = self.get_facing(direction)

        target_tile, target_xy = self.get_adjacent_tile(new_facing)

        self.facing = new_facing
        if target_tile.rect.collidepoint(self.rect.center) == True:
            self.current_tile = target_tile
            self.tile_xy = target_xy

        # Allow moving from left to right OR up and down
        if target_tile.rect.centery ==  self.rect.centery or target_tile.rect.centerx ==  self.rect.centerx:
            self.rect.move_ip(direction)

        if self.name == "Pacman":
            points_list = pygame.sprite.spritecollide(self,pointsGroup,True)
            for point in points_list:
                self.score += 1
        return True

    def can_move_to(self,direction):
        new_facing = self.get_facing(direction)
        target_tile, target_xy = self.get_adjacent_tile(new_facing)
        if target_tile.isWalkable() == False:
            return False
        if new_facing == FACING_UP or new_facing == FACING_DOWN:
            if target_tile.rect.centerx != self.rect.centerx:
                return False
        elif new_facing == FACING_LEFT or new_facing == FACING_RIGHT:
            if target_tile.rect.centery != self.rect.centery:
                return False
        return True

    def __del__(self):
        print 'Destructor'

# Blinky is the red ghost
class Blinky(Character):
    def __init__(self, FILENAME, boardMatrix):
        Character.__init__(self, FILENAME, boardMatrix)
        self.name = "Blinky"
        # Every ghost needs the following three lines of code
        self.tile_xy = (14,14)
        self.current_tile = boardMatrix[self.tile_xy[0]][self.tile_xy[1]]
        self.rect.center = self.current_tile.getCenter()
        self.current_direction = GO_LEFT
        self.last_kg_direction = 0
        print 'Blinky constructor'

    def get_direction_from_to(self,from_tile, to_tile):
        if from_tile.rect.centerx and to_tile.rect.centerx:
            if to_tile.rect.centerx < from_tile.rect.centerx:
                return GO_LEFT
            if to_tile.rect.centerx > from_tile.rect.centerx:
                return GO_RIGHT
        if from_tile.rect.centery and to_tile.rect.centery:
            if to_tile.rect.centery < from_tile.rect.centery:
                return GO_UP
            if to_tile.rect.centery > from_tile.rect.centery:
                return GO_DOWN
        return STAND_STILL

    def update(self):
        global POINTS_LIST
        #Implement custom behavior, then call base class method
        target_tile = Character.PACMAN.current_tile
        adjacent_tile, tile_xy = self.get_adjacent_tile(self.facing)
        # TODO: Add code to handle special intersections
        if adjacent_tile.is_intersection:
            self.current_direction = self.get_closest_direction(adjacent_tile, target_tile)

        if self.movedirection(self.current_direction, POINTS_LIST) == True:
            self.last_kg_direction = self.current_direction
        else:
            if self.movedirection(self.last_kg_direction, POINTS_LIST) == False:
                self.current_direction = self.get_closest_direction(self.current_tile, target_tile)

        if Character.PACMAN.rect.collidepoint(self.rect.center):
            print "GAME OVER"
        
        Character.update(self)

    def __del__(self):
        print 'Blinky destructor'

    def get_closest_direction(self, from_tile, to_tile):
        """
        Gets the neighbors from tile from_tile, and then determines the closest tile to to_tile.
        :param from_tile:
        :param to_tile:
        """
        neighbors = get_tile_neighbors(self.board_matrix, from_tile)
        # neighbors.remove(self.current_tile) This line may or may not cause a bug, watch out
        d_list = []
        for tile in neighbors:
            distance = self.pitagorazo(tile.rect.centerx-to_tile.rect.centerx,
                                       tile.rect.centery-to_tile.rect.centery)
            d_list.append(distance)
        closest = min(d_list)
        index = d_list.index(closest)

        return self.get_direction_from_to(from_tile,neighbors[index])

    def pitagorazo(self, a, b):
        c = sqrt(pow(a,2) + pow(b,2))
        return c

# Pinky is the pink ghost
class Pinky(Character):
    def __init__(self, FILENAME, boardMatrix):
        Character.__init__(self, FILENAME, boardMatrix)
        self.name = "Pink"
        # Every ghost needs the following three lines of code
        self.tile_xy = (13,17)
        self.current_tile = boardMatrix[self.tile_xy[0]][self.tile_xy[1]]
        self.rect.center = self.current_tile.getCenter()
        self.current_direction = GO_LEFT
        self.last_kg_direction = 0
        print 'Pinky constructor'

    def update(self):
        #Implement custom behavior, then call base class method
        Character.update(self)

    def __del__(self):
        print 'Pink destructor'

# Inky is the cyan ghost
class Inky(Character):
    def __init__(self, FILENAME):
        Character.__init__(self, FILENAME)
        self.name = "Inky"
        print 'Inky constructor'

    def update(self):
        #Implement custom behavior, then call base class method
        Character.update(self)

    def __del__(self):
        print 'Inky destructor'

# Clyde is the orange ghost
class Clyde(Character):
    def __init__(self, FILENAME):
        Character.__init__(self, FILENAME)
        self.name = "Clyde"
        print 'Clyde constructor'

    def update(self):
        #Implement custom behavior, then call base class method
        Character.update(self)

    def __del__(self):
        print 'Clyde destructor'

# Pacman is pacman
class Pacman(Character):
    def __init__(self, FILENAME, boardMatrix):
        Character.__init__(self, FILENAME, boardMatrix)
        self.name = "Pacman"
        self.score = 0
        self.tile_xy = (13,26)
        self.current_tile = boardMatrix[self.tile_xy[0]][self.tile_xy[1]]
        self.rect.center = self.current_tile.getCenter()
        Character.PACMAN = self
        print 'Pacman constructor'

    def update(self):
        #Implement custom behavior, then call base class method
        Character.update(self)


    def __del__(self):
        print 'Pacman destructor'

def get_characters_group(boardMatrix, wallSpriteGroup, pointsGroup):
    global PACMAN
    global WALL_LIST
    global POINTS_LIST
    WALL_LIST = wallSpriteGroup
    POINTS_LIST = pointsGroup

    PACMAN = pacman = Pacman("pacman1.png", boardMatrix)

    blinky = Blinky("rojo.png", boardMatrix)
    pinky = Pinky("rosa.png", boardMatrix)


    ghostsprite = pygame.sprite.RenderPlain()
    #ghostsprite.add(blinky)
    ghostsprite.add(pinky)
    ghostsprite.add(pacman)
    return ghostsprite, pacman
