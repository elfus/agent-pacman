#! /usr/bin/python


__author__ = 'aortegag'

import pygame
from pygame.locals import *
from util import *
from pacman_maze import *
from characters import *

X_AXIS = 0
Y_AXIS = 1

LAST_DIRECTION = GO_LEFT
PENDING_DIRECTION = GO_LEFT

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
    global PENDING_DIRECTION
    direction = PENDING_DIRECTION
    if pygame.key.get_pressed()[pygame.K_w]:
        direction = GO_UP
    elif pygame.key.get_pressed()[pygame.K_s]:
        direction = GO_DOWN
    elif pygame.key.get_pressed()[pygame.K_a]:
        direction = GO_LEFT
    elif pygame.key.get_pressed()[pygame.K_d]:
        direction = GO_RIGHT

    return direction

def next_mode():
    print "Changing game mode"
    Character.CURRENT_MODE = (Character.CURRENT_MODE+1) % NUMBER_MODE
    return
def main():
    global LAST_DIRECTION
    global PENDING_DIRECTION

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

    detect_walkable_tiles(board_matrix, wallSpriteGroup)

    detect_intersections(board_matrix)

    ghostsprite, pacman = get_characters_group(board_matrix, wallSpriteGroup, pointsGroup)

    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)

        ## Used for debugging
        for row in board_matrix:
            for tile in row:
                # if tile.isWalkable() == True:
                #     screen.fill(PURPLE, tile.rect)
                if tile.is_special_intersection == True:
                    screen.fill(GREEN, tile.rect)
                elif tile.is_intersection == True:
                    screen.fill(WHITE, tile.rect)

                if tile.is_in_ghost_house:
                    screen.fill(PURPLE,tile.rect)

                if tile.is_clyde_switch_mode:
                    screen.fill(PURPLE,tile.rect)
        ## Used for debugging

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
                # For some reason when detecting the keyboard with these 2 lines, pacman moves
                # slower, why? I don't know and I don't want to investigate, for the moment
                # let's use this workaround
                # direction = handle_event(event)
                # pacman.movedirection(direction, wallSpriteGroup, pointsGroup)
                print "Pacman coordinate: ", pacman.rect
                if event.key == pygame.K_m:
                    next_mode()

        # When detecting keyboard here, pacman moves faster
        direction = handle_input()
        if pacman.movedirection(direction, pointsGroup) == True:
            LAST_DIRECTION  = PENDING_DIRECTION = direction
        else:
            pacman.movedirection(LAST_DIRECTION, pointsGroup)
            PENDING_DIRECTION = direction

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