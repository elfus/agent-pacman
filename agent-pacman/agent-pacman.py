#! /usr/bin/python
import os
import math

__author__ = 'aortegag'

import pygame
from pygame.locals import *

OFFSET = 4
X_AXIS = 0
Y_AXIS = 1

BLACK  = (   0,   0,   0)
WHITE  = ( 255, 255, 255)
BLUE   = (   0,   0, 255)
GREEN  = (   0, 255,   0)
RED    = ( 255,   0,   0)
PURPLE = ( 255,   0, 255)

PACMAN_START = (107,207)
GHOST_START = (105,133)

def handle_event(event):
    """
    Handles a pygame.K_DOWN event
    :param event: A pygame.event
    :return: The direction in whic pacman has to move
    """
    direction = [0, 0]
    if event.key == pygame.K_w:
        direction = [0, -OFFSET]
    elif event.key == pygame.K_s:
        direction = [0, OFFSET]
    elif event.key == pygame.K_a:
        direction = [-OFFSET, 0]
    elif event.key == pygame.K_d:
        direction = [OFFSET, 0]
    return direction


def handle_input():
    """
    Detects the keys pressed using PyGame to move describe a direction

    :return: The direction where to move
    """
    direction = [0, 0]
    if pygame.key.get_pressed()[pygame.K_w]:
        direction = [0, -OFFSET]
    elif pygame.key.get_pressed()[pygame.K_s]:
        direction = [0, OFFSET]
    elif pygame.key.get_pressed()[pygame.K_a]:
        direction = [-OFFSET, 0]
    elif pygame.key.get_pressed()[pygame.K_d]:
        direction = [OFFSET, 0]

    return direction


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


class Ghost(pygame.sprite.Sprite):
    """A Ghost that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("rojo.png")
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.stop()
        print 'Constructor'

    def stop(self):
        self.movepos = [0, 0]
        self.state = "still"

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

    def moveup(self):
        self.movepos = [0, -OFFSET]
        self.state = "moveup"

    def movedown(self):
        self.movepos = [0, OFFSET]
        self.state = "movedown"


    def moveleft(self):
        self.movepos = [-OFFSET, 0]
        self.state = "moveleft"

    def moveright(self):
        self.movepos = [OFFSET, 0]
        self.state = "moveright"

    def __del__(self):
        print 'Destructor'

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
                if len(pygame.sprite.spritecollide(wall,wallSpriteGroup,False)) == 0:
                    wallSpriteGroup.add(wall)
            w += 1
        h += 1

    print "Number of rectangles ", len(wallSpriteGroup.sprites())
    return wallSpriteGroup


def main():
    pygame.init()

    pacman_background = pygame.image.load("res/tableropacman.jpg")
    pacman_rect = pacman_background.get_rect()
    window_size = width, height = pacman_background.get_width(), pacman_background.get_height()

    # Create a graphical window by calling set_mode
    # Pygame represents images as Surface objects. The "display.set_mode()"
    # function creates a new Surface object that represents the actual
    # displayed graphics. Any drawing you do to this Surface will become
    # visible on the monitor.
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Agent Pacman")

    ball, ballrect = load_image("rojo.png")

    # Convert the pixel formats to that of the same type as our screen.
    ball = ball.convert_alpha()  # Convert_alpha keeps the alpha channel in the pixel
    pacman_background = pacman_background.convert_alpha()  # Removes alpha channel

    screen.blit(pacman_background, pacman_rect)
    # NOTE: Try commenting out this line and see how input behaves
    pygame.key.set_repeat(50, 50)

    ghost = Ghost()
    ghostsprite = pygame.sprite.RenderPlain(ghost)
    newpos = ghost.rect.move(GHOST_START)
    if ghost.area.contains(newpos):
        ghost.rect = newpos

    clock = pygame.time.Clock()
    direction = [0, 0]

    wallSpriteGroup = analyze_maze()

    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)
        screen.blit(pacman_background, ghost.rect, ghost.rect)
        # Detect the input and get a new direction
        # NOTE: This is the line that will be replaced by the agents once they are implemented
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                direction = handle_event(event)
                ghost.movedirection(direction, wallSpriteGroup)
            if event.type == pygame.KEYUP:
                if event.key == K_w or event.key == K_s or event.key == K_a or event.key == K_d:
                    ghost.stop()



        ghost.update()
        ghostsprite.draw(screen)
        wallSpriteGroup.draw(screen)

        # PyGame uses a double buffer to display images on screen
        # since we were drawing the back buffer it's time to flip it
        # and make it available on the front buffer
        pygame.display.flip()


if __name__ == "__main__":
    main()