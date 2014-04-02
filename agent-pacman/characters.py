__author__ = 'aortegag'

import pygame
from pygame.locals import *
from pygame.locals import *
from util import *

PACMAN_START = (105,206)
GHOST_START = (105,133)

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

    def movedirection(self, direction, wallPixels):
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

    def __del__(self):
        print 'Destructor'

# Blinky is the red ghost
class Blinky(Character):
    def __init__(self, FILENAME):
        Character.__init__(self, FILENAME)
        self.name = "Blinky"
        print 'Blinky constructor'

    def update(self):
        #Implement custom behavior, then call base class method
        Character.update(self)

    def __del__(self):
        print 'Blinky destructor'

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
        print 'Pacman constructor'

    def update(self):
        #Implement custom behavior, then call base class method
        Character.update(self)

    def __del__(self):
        print 'Pacman destructor'

def get_characters_group():
    blinky = Blinky("rojo.png")
    blinky.rect = blinky.rect.move(GHOST_START)

    pacman = Pacman("pacman.png")
    pacman.rect = pacman.rect.move(PACMAN_START)

    ghostsprite = pygame.sprite.RenderPlain(blinky)
    ghostsprite.add(pacman)
    return ghostsprite, pacman
