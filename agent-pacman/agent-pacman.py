#! /usr/bin/python


__author__ = 'aortegag'

import pygame
from pygame.locals import *
from util import *
from pacman_maze import *
from characters import *


OFFSET = 4
X_AXIS = 0
Y_AXIS = 1

GO_LEFT = [-OFFSET, 0]
GO_RIGHT = [OFFSET, 0]
GO_DOWN = [0, OFFSET]
GO_UP = [0, -OFFSET]

def handle_event(event):
    """
    Handles a pygame.K_DOWN event
    :param event: A pygame.event
    :return: The direction in whic pacman has to move
    """
    direction = [0, 0]
    if event.key == pygame.K_w:
        direction = GO_UP
    elif event.key == pygame.K_s:
        direction = GO_DOWN
    elif event.key == pygame.K_a:
        direction = GO_LEFT
    elif event.key == pygame.K_d:
        direction = GO_RIGHT
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

    pacman_background = pygame.image.load("res/tableropacman.jpg")
    pacman_rect = pacman_background.get_rect()
    window_size = width, height = pacman_background.get_width(), pacman_background.get_height()
    board_matrix = create_board_matrix(width,height)

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

    clock = pygame.time.Clock()
    direction = [0, 0]

    wallSpriteGroup, pointsGroup = analyze_maze()

    ghostsprite, pacman = get_characters_group(board_matrix, wallSpriteGroup, pointsGroup)

    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)

        for character in ghostsprite.sprites():
            screen.blit(pacman_background, character.rect, character.rect)

        # Detect the input and get a new direction
        # NOTE: This is the line that will be replaced by the agents once they are implemented
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                direction = handle_event(event)
                pacman.movedirection(direction, wallSpriteGroup, pointsGroup)
                print "Pacman coordinate: ", pacman.rect
            if event.type == pygame.KEYUP:
                if event.key == K_w or event.key == K_s or event.key == K_a or event.key == K_d:
                    pacman.stop()

        ghostsprite.update()
        ghostsprite.draw(screen)
        # Comment out this line to remove collition detection debugging
        # wallSpriteGroup.draw(screen)
        pointsGroup.draw(screen)

        # PyGame uses a double buffer to display images on screen
        # since we were drawing the back buffer it's time to flip it
        # and make it available on the front buffer
        pygame.display.flip()


if __name__ == "__main__":
    main()