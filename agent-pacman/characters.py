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

    def get_adjacent_tile(self):
        """
        Gets the adjacent tile to this character depending on where it is facing.
        This variable assumes the attribute variable self.facing is set before
        calling this method.

        :rtype : The tile (Rect) object adjacent where the character is facing
        :return: The tile coordinates in the board matrix
        """
        adjacent_tile = 0
        target_tile = (-1,-1)

        if self.facing == FACING_LEFT:
            target_tile = (self.tile_xy[0]-1,self.tile_xy[1])
        elif self.facing == FACING_RIGHT:
            target_tile = (self.tile_xy[0]+1,self.tile_xy[1])
        elif self.facing == FACING_UP:
            target_tile = (self.tile_xy[0],self.tile_xy[1]-1)
        elif self.facing == FACING_DOWN:
            target_tile = (self.tile_xy[0],self.tile_xy[1]+1)

        if target_tile[0] >= TILE_WIDTH_COUNT:
            target_tile[0] = TILE_WIDTH_COUNT - 1

        if target_tile[1] >= TILE_HEIGHT_COUNT:
            target_tile[1] = TILE_HEIGHT_COUNT - 1

        adjacent_tile = self.board_matrix[target_tile[0]][target_tile[1]]
        if adjacent_tile.isWalkable() == False:
            print "Tile coordinates ",target_tile," facing ",self.facing," is NOT walkable"

        return adjacent_tile, target_tile

    def collides(self, direction):
        old_rect = self.rect.copy()
        self.rect.x += direction[0]
        collitionDetected = False
        hit_wall_list = pygame.sprite.spritecollide(self,WALL_LIST,False)
        if len(hit_wall_list) > 0:
            collitionDetected = True

        self.rect.y += direction[1]
        hit_wall_list = pygame.sprite.spritecollide(self,WALL_LIST,False)
        if len(hit_wall_list) > 0:
            collitionDetected = True

        self.rect = old_rect.copy()
        return collitionDetected

    def __del__(self):
        print 'Destructor'

# Blinky is the red ghost
class Blinky(Character):
    def __init__(self, FILENAME, boardMatrix):
        Character.__init__(self, FILENAME, boardMatrix)
        self.name = "Blinky"
        print 'Blinky constructor'

    def update(self):
        global WALL_LIST
        global POINTS_LIST
        #Implement custom behavior, then call base class method
        # direction = self.finddirection(self.rect.center, PACMAN.rect.center)
        # self.movedirection(direction, WALL_LIST, POINTS_LIST)
        Character.update(self)

    def __del__(self):
        print 'Blinky destructor'

    def finddirection(self, from_pos, to_pos ):
        pos1 = (from_pos[0], from_pos[1]-1)
        pos2 = (from_pos[0]+1, from_pos[1])
        pos3 = (from_pos[0], from_pos[1]+1)
        pos4 = (from_pos[0]-1, from_pos[1])
        distance_list = [self.pitagorazo(pos1[0]-to_pos[0], pos1[1]-to_pos[1]),
                self.pitagorazo(pos2[0]-to_pos[0], pos2[1]-to_pos[1]),
                self.pitagorazo(pos3[0]-to_pos[0], pos3[1]-to_pos[1]),
                self.pitagorazo(pos4[0]-to_pos[0], pos4[1]-to_pos[1]),
                ]
        new_list = list(distance_list)
        new_list.sort()
        for direction in new_list:
            new_direction = 0;
            if distance_list.index(direction) == INDEX_UP:
                new_direction = DIRECTION_UP
            elif distance_list.index(direction) == INDEX_RIGHT:
                new_direction = DIRECTION_RIGHT
            elif distance_list.index(direction) == INDEX_DOWN:
                new_direction = DIRECTION_DOWN
            elif distance_list.index(direction) == INDEX_LEFT:
                new_direction = DIRECTION_LEFT

            if self.collides(new_direction) == False:
                return new_direction
            else:
                return [0,0]

    def pitagorazo(self, a, b):
        c = sqrt(pow(a,2) + pow(b,2))
        return c

# Pinky is the pink ghost
class Pink(Character):
    def __init__(self, FILENAME):
        Character.__init__(self, FILENAME)
        self.name = "Pink"
        print 'Pink constructor'

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
        print 'Pacman constructor'

    def update(self):
        #Implement custom behavior, then call base class method
        Character.update(self)

    def movedirection(self, direction, wallPixels, pointsGroup):
        if direction == DIRECTION_LEFT: self.facing = FACING_LEFT
        if direction == DIRECTION_RIGHT: self.facing = FACING_RIGHT
        if direction == DIRECTION_UP: self.facing = FACING_UP
        if direction == DIRECTION_DOWN: self.facing = FACING_DOWN

        target_tile, target_xy = self.get_adjacent_tile()
        if target_tile.isWalkable() == False:
            return

        if target_tile.rect.collidepoint(self.rect.center) == True:
            self.current_tile = target_tile
            self.tile_xy = target_xy

        # Allow moving from left to right OR up and down
        print "target_tile.center: ",target_tile.rect.center," -- pacman.rect.center: ",self.rect.center
        if target_tile.rect.centery ==  self.rect.centery:
            self.rect.move_ip(direction)
        elif target_tile.rect.centerx ==  self.rect.centerx:
            self.rect.move_ip(direction)

        #################################
        # self.rect.x += direction[0]
        # hit_wall_list = pygame.sprite.spritecollide(self,wallPixels,False)
        # # check for any collision with a wall
        # for wall in hit_wall_list:
        #     if direction[0] > 0:
        #         self.rect.right = wall.rect.left
        #     else:
        #         self.rect.left = wall.rect.right
        #
        #     if wall.image.get_at([0,0]) == pygame.Color("green"):
        #         wall.image.fill(PURPLE)
        #     else:
        #         wall.image.fill(GREEN)
        #
        # self.rect.y += direction[1]
        # hit_wall_list = pygame.sprite.spritecollide(self,wallPixels,False)
        # # check for any collision with a wall
        # for wall in hit_wall_list:
        #     if direction[1] > 0:
        #         self.rect.bottom = wall.rect.top
        #     else:
        #         self.rect.top = wall.rect.bottom
        #
        #     if wall.image.get_at([0,0]) == pygame.Color("green"):
        #         wall.image.fill(PURPLE)
        #     else:
        #         wall.image.fill(GREEN)

        print "Facing ", self.facing


        if self.name == "Pacman":
            points_list = pygame.sprite.spritecollide(self,pointsGroup,True)
            for point in points_list:
                self.score += 1

    def __del__(self):
        print 'Pacman destructor'

def get_characters_group(boardMatrix, wallSpriteGroup, pointsGroup):
    global PACMAN
    global WALL_LIST
    global POINTS_LIST
    WALL_LIST = wallSpriteGroup
    POINTS_LIST = pointsGroup

    blinky = Blinky("rojo.png", boardMatrix)
    blinky.rect = blinky.rect.move(BLINKY_START)

    PACMAN = pacman = Pacman("pacman1.png", boardMatrix)


    ghostsprite = pygame.sprite.RenderPlain(blinky)
    ghostsprite.add(pacman)
    return ghostsprite, pacman
