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
BLINKY_START = (107, 108)

PACMAN = 0

INDEX_UP = 0
INDEX_RIGHT = 1
INDEX_DOWN = 2
INDEX_LEFT = 3

OFFSET = 4
DIRECTION_UP = [0, -OFFSET]
DIRECTION_RIGHT = [OFFSET, 0]
DIRECTION_DOWN = [0, OFFSET]
DIRECTION_LEFT = [-OFFSET, 0]


class Character(pygame.sprite.Sprite):
    """A Ghost that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(self, FILENAME):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(FILENAME)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.stop()
        self.name = "Character"
        print 'Character Constructor'

    def stop(self):
        self.movepos = [0, 0]
        self.state = "still"

    def update(self):
        # This is if is meant to detect the case in which any character goes through
        # the 'middle tunnel' on the maze and appears on the other side
        if self.area.contains(self.rect) == False:
            if self.rect.left < (self.area.left - self.rect.width):
                self.rect.left = self.area.right
                return
            if self.rect.right > (self.area.right + self.rect.width):
                self.rect.right = self.area.left
                return

    def movedirection(self, direction, wallPixels, pointsGroup):
        self.rect.x += direction[0]
        hit_wall_list = pygame.sprite.spritecollide(self,wallPixels,False)
        # check for any collision with a wall
        for wall in hit_wall_list:
            if direction[0] > 0:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right

            if wall.image.get_at([0,0]) == pygame.Color("green"):
                wall.image.fill(PURPLE)
            else:
                wall.image.fill(GREEN)

        self.rect.y += direction[1]
        hit_wall_list = pygame.sprite.spritecollide(self,wallPixels,False)
        # check for any collision with a wall
        for wall in hit_wall_list:
            if direction[1] > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom

            if wall.image.get_at([0,0]) == pygame.Color("green"):
                wall.image.fill(PURPLE)
            else:
                wall.image.fill(GREEN)

        if self.name == "Pacman":
            points_list = pygame.sprite.spritecollide(self,pointsGroup,True)
            for point in points_list:
                self.score += 1
                print "Score ",self.score," points"

    def __del__(self):
        print 'Destructor'

# Blinky is the red ghost
class Blinky(Character):
    def __init__(self, FILENAME):
        Character.__init__(self, FILENAME)
        self.name = "Blinky"
        print 'Blinky constructor'

    def update(self):
        global WALL_LIST
        global POINTS_LIST
        #Implement custom behavior, then call base class method
        direction = self.finddirection(self.rect.center, PACMAN.rect.center)
        self.movedirection(direction, WALL_LIST, POINTS_LIST)
        Character.update(self)

    def __del__(self):
        print 'Blinky destructor'

    def finddirection(self, from_pos, to_pos ):
        print "Current pos ", from_pos," want to move to ", to_pos
        pos1 = (from_pos[0], from_pos[1]-1)
        pos2 = (from_pos[0]+1, from_pos[1])
        pos3 = (from_pos[0], from_pos[1]+1)
        pos4 = (from_pos[0]-1, from_pos[1])
        list = [self.pitagorazo(pos1[0]-to_pos[0], pos1[1]-to_pos[1]),
                self.pitagorazo(pos2[0]-to_pos[0], pos2[1]-to_pos[1]),
                self.pitagorazo(pos3[0]-to_pos[0], pos3[1]-to_pos[1]),
                self.pitagorazo(pos4[0]-to_pos[0], pos4[1]-to_pos[1]),
                ]
        direction = min(list)
        if list.index(direction) == INDEX_UP:
            return DIRECTION_UP
        elif list.index(direction) == INDEX_RIGHT:
            return DIRECTION_RIGHT
        elif list.index(direction) == INDEX_DOWN:
            return DIRECTION_DOWN
        elif list.index(direction) == INDEX_LEFT:
            return DIRECTION_LEFT

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
    def __init__(self, FILENAME):
        Character.__init__(self, FILENAME)
        self.name = "Pacman"
        self.score = 0
        print 'Pacman constructor'

    def update(self):
        #Implement custom behavior, then call base class method
        Character.update(self)

    def __del__(self):
        print 'Pacman destructor'

def get_characters_group(wallSpriteGroup, pointsGroup):
    global PACMAN
    global WALL_LIST
    global POINTS_LIST
    WALL_LIST = wallSpriteGroup
    POINTS_LIST = pointsGroup

    blinky = Blinky("rojo.png")
    blinky.rect = blinky.rect.move(BLINKY_START)

    PACMAN = pacman = Pacman("pacman1.png")
    pacman.rect = pacman.rect.move(PACMAN_START)

    ghostsprite = pygame.sprite.RenderPlain(blinky)
    ghostsprite.add(pacman)
    return ghostsprite, pacman