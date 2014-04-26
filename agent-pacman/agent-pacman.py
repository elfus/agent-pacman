#! /usr/bin/python


__author__ = 'aortegag'

import pygame
from pygame.locals import *
from util import *
from pacman_maze import *
from characters import *
import time

X_AXIS = 0
Y_AXIS = 1

LAST_DIRECTION = GO_LEFT
PENDING_DIRECTION = GO_LEFT

CURRENT_MODE_START = time.time()
CURRENT_MODE_END = 0
STATUS_MSG_COORDINATES = ((BOARD_WIDTH/2),(BOARD_HEIGHT-8))

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
    if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP]:
        direction = GO_UP
    elif pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]:
        direction = GO_DOWN
    elif pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
        direction = GO_LEFT
    elif pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
        direction = GO_RIGHT

    return direction

def render_score(screen, score, center):
    """
    Renders pacman score on screen
    :param screen: Surface screen
    """
    font = pygame.font.Font(None,20)
    text = font.render(score, 1, (220,252,199))
    textrect = text.get_rect()
    textrect.center = center
    screen.fill((0,0,0),  pygame.Rect(textrect.left-10,textrect.top,textrect.width+20,textrect.height))
    screen.blit(text, textrect)

def render_message(screen, msg="", center=STATUS_MSG_COORDINATES, font_size=20):
    """
    Renders pacman score on screen
    :param screen: Surface screen
    :param
    """
    font = pygame.font.Font(None,font_size)
    text = font.render(msg, 1, (220,252,199))
    textrect = text.get_rect()
    textrect.center = center
    if len(msg) == 0:
        textrect.width = BOARD_WIDTH
        textrect.x = 0
    screen.fill((0,0,0), textrect )
    screen.blit(text, textrect)

def ghost_mode_detector():
    global CURRENT_MODE_START
    global CURRENT_MODE_END

    if Character.CHANGE_TO_FRIGHTENED == True:
        Character.CHANGE_TO_FRIGHTENED = False
        change_mode(FRIGHTENED_MODE)
        CURRENT_MODE_START = time.time()

    CURRENT_MODE_END = time.time()
    elapsed_time = CURRENT_MODE_END - CURRENT_MODE_START

    if Character.CURRENT_MODE == CHASE_MODE:
        if elapsed_time > 20.0:
            change_mode(SCATTER_MODE)
            CURRENT_MODE_START = time.time()
            print "Elapsed time",elapsed_time,"seconds"
    elif Character.CURRENT_MODE == SCATTER_MODE:
        if elapsed_time > 7.0:
            change_mode(CHASE_MODE)
            CURRENT_MODE_START = time.time()
            print "Elapsed time",elapsed_time,"seconds"
    elif Character.CURRENT_MODE == FRIGHTENED_MODE:
        if elapsed_time > 7.0:
            change_mode(CHASE_MODE)
            CURRENT_MODE_START = time.time()
            print "Elapsed time",elapsed_time,"seconds"

def main():
    global LAST_DIRECTION
    global PENDING_DIRECTION
    PAUSE_GAME = False
    STARTING_GAME = True
    COUNTDOWN = 3
    PLAYER_CHOSEN = False
    PLAYER_HUMAN = "Human"
    PLAYER_COMPUTER = "Computer"
    PLAYER_NA = "na"
    CURRENT_PLAYER = PLAYER_NA
    BOARD_RIGHT_PADDING = 300

    pygame.init()

    pacman_background = pygame.image.load("res/tableropacman.jpg")
    pacman_rect = pacman_background.get_rect()
    window_size = BOARD_WIDTH, BOARD_HEIGHT = pacman_background.get_width(), pacman_background.get_height()
    board_matrix = create_board_matrix(BOARD_WIDTH,BOARD_HEIGHT)

    # Create a graphical window by calling set_mode
    # Pygame represents images as Surface objects. The "display.set_mode()"
    # function creates a new Surface object that represents the actual
    # displayed graphics. Any drawing you do to this Surface will become
    # visible on the monitor.
    screen = pygame.display.set_mode((BOARD_WIDTH+BOARD_RIGHT_PADDING,BOARD_HEIGHT))
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

    ghostsprite, pacman = get_characters_group(board_matrix, pointsGroup)

    pointsGroup = generate_pacman_points(board_matrix)

    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)

        ## Used for debugging
        # for row in board_matrix:
        #     for tile in row:
        #         # if tile.isWalkable() == True:
        #         #     screen.fill(PURPLE, tile.rect)
        #         if tile.is_special_intersection == True:
        #             screen.fill(GREEN, tile.rect)
        #         elif tile.is_intersection == True:
        #             screen.fill(WHITE, tile.rect)
        #
        #         if tile.is_in_ghost_house:
        #             screen.fill(PURPLE,tile.rect)
        #
        #         if tile.is_scatter_tile:
        #             screen.fill(PURPLE,tile.rect)
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
                # print "Pacman coordinate: ", pacman.rect
                if event.key == pygame.K_m:
                    next_mode()
                elif event.key == pygame.K_h:
                    CURRENT_PLAYER = PLAYER_HUMAN
                elif event.key == pygame.K_c:
                    CURRENT_PLAYER = PLAYER_COMPUTER
                elif event.key == pygame.K_j:
                    change_mode(CHASE_MODE)
                elif event.key == pygame.K_k:
                    change_mode(SCATTER_MODE)
                elif event.key == pygame.K_l:
                    change_mode(FRIGHTENED_MODE)
                elif event.key == pygame.K_p:
                    PAUSE_GAME = not PAUSE_GAME
                    if PAUSE_GAME == False:
                        render_message(screen)

        if PLAYER_CHOSEN == False:
            render_message(screen, "Press H for Human, C for Computer",font_size=18)
            screen.fill((123,140,140),pygame.Rect(BOARD_WIDTH,0,BOARD_RIGHT_PADDING,BOARD_HEIGHT))
            pygame.display.flip()
            if CURRENT_PLAYER == PLAYER_COMPUTER or CURRENT_PLAYER == PLAYER_HUMAN:
                render_message(screen)
                render_message(screen,"Player type chosen: "+CURRENT_PLAYER)
                pygame.display.flip()
                pygame.time.delay(2000)
                render_message(screen)
                PLAYER_CHOSEN = True
            continue

        if STARTING_GAME:
            ghostsprite.draw(screen)
            render_message(screen, "Starting game in "+str(COUNTDOWN))
            screen.fill((123,140,140),pygame.Rect(BOARD_WIDTH,0,BOARD_RIGHT_PADDING,BOARD_HEIGHT))
            pointsGroup.draw(screen)
            render_score(screen, str(Character.PACMAN.score), (30,16))
            render_score(screen, str(Character.PACMAN.highest_score), ((BOARD_WIDTH/2),16))
            pygame.display.flip()
            pygame.time.delay(1000)
            COUNTDOWN -= 1
            if COUNTDOWN == 0:
                STARTING_GAME = False
                COUNTDOWN = 3
                render_message(screen)
            continue

        if PAUSE_GAME:
            ghostsprite.draw(screen)
            render_message(screen, "Press P to unpause the game")
            screen.fill((123,140,140),pygame.Rect(BOARD_WIDTH,0,BOARD_RIGHT_PADDING,BOARD_HEIGHT))
            pointsGroup.draw(screen)
            render_score(screen, str(Character.PACMAN.score), (30,16))
            render_score(screen, str(Character.PACMAN.highest_score), ((BOARD_WIDTH/2),16))
            pygame.display.flip()
            continue

        # When detecting keyboard here, pacman moves faster
        direction = handle_input()
        if pacman.movedirection(direction, pointsGroup) == True:
            LAST_DIRECTION  = PENDING_DIRECTION = direction
        else:
            pacman.movedirection(LAST_DIRECTION, pointsGroup)
            PENDING_DIRECTION = direction

        ghostsprite.update()
        ghostsprite.draw(screen)
        # workaround to make sure when any character exits on the right side of the tunnel,
        # it's always black
        screen.fill((123,140,140),pygame.Rect(BOARD_WIDTH,0,BOARD_RIGHT_PADDING,BOARD_HEIGHT))
        pointsGroup.draw(screen)

        render_score(screen, str(Character.PACMAN.score), (30,16))
        render_score(screen, str(Character.PACMAN.highest_score), ((BOARD_WIDTH/2),16))

        if(Character.GAME_OVER):
            pygame.time.delay(1000)
            Character.PACMAN.score = 0
            render_score(screen, str(Character.PACMAN.score), (30,16))
            render_score(screen, str(Character.PACMAN.highest_score), ((BOARD_WIDTH/2),16))
            pointsGroup = generate_pacman_points(board_matrix)
            Character.GAME_OVER = False
            change_mode(CHASE_MODE)
            STARTING_GAME = True
            render_message(screen,"GAME OVER!")
            pygame.display.flip()
            pygame.time.delay(2000)


        ghost_mode_detector()
        # PyGame uses a double buffer to display images on screen
        # since we were drawing the back buffer it's time to flip it
        # and make it available on the front buffer
        pygame.display.flip()


if __name__ == "__main__":
    main()