#! /usr/bin/python
__author__ = 'aortegag'

import pygame
import pygame.constants
from pygame.locals import *

OFFSET = 3
X_AXIS = 0
Y_AXIS = 1

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

def main():
    pygame.init()

    ball = pygame.image.load("res/rojo.png")
    ballrect = ball.get_rect()

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

    # Convert the pixel formats to that of the same type as our screen.
    ball = ball.convert_alpha() # Convert_alpha keeps the alpha channel in the pixel
    pacman_background = pacman_background.convert_alpha() # Removes alpha channel

    screen.blit(pacman_background,pacman_rect)
    pygame.key.set_repeat(50,50)
    while 1:
        direction = [0,0]
        # Detect the input and get a new direction
        # NOTE: This is the line that will be replaced by the agents once they are implemented
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                direction = handle_event(event)

         # Fill the background that was erased by the ball
        screen.blit(pacman_background,ballrect,ballrect)

        # The class pygame.Rect is a rectanble represeting the position of the ball
        ballrect.move_ip(direction)

        # If we are out of boundaries stay inside
        if ballrect.left < 0 or ballrect.right > width:
            if ballrect.left < 0:
                ballrect.left = 0
            if ballrect.right > width:
                ballrect.right = width
        if ballrect.top < 0 or ballrect.bottom > height:
            if ballrect.top < 0:
                ballrect.top = 0
            if ballrect.bottom > height:
                ballrect.bottom = height

        # Draw the ball image onto the screen. We pass the blit method a
        # source Surface to copy from, and a position to place the source
        # onto the destination.
        screen.blit(ball, ballrect)

        # PyGame uses a double buffer to display images on screen
        # since we were drawing the back buffer it's time to flip it
        # and make it available on the front buffer
        pygame.display.flip()

if __name__ == "__main__":
    main()