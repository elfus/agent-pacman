#! /usr/bin/python
__author__ = 'aortegag'

import sys, pygame

OFFSET = 1
X_AXIS = 0
Y_AXIS = 1

def handle_input():
    """
    Detects the keys pressed using PyGame to move describe a direction

    :return: The direction where to move
    """
    direction = [0, 0]
    if pygame.key.get_pressed()[pygame.K_w]:
        direction = [0, -OFFSET]
    if pygame.key.get_pressed()[pygame.K_s]:
        direction = [0, OFFSET]
    if pygame.key.get_pressed()[pygame.K_a]:
        direction = [-OFFSET, 0]
    if pygame.key.get_pressed()[pygame.K_d]:
        direction = [OFFSET, 0]

    return direction

def main():
    pygame.init()

    ball = pygame.image.load("res/ball.gif")
    ballrect = ball.get_rect()

    pacman_background = pygame.image.load("res/pac-man-background.jpg")
    pacman_rect = pacman_background.get_rect()
    window_size = width, height = pacman_background.get_width(), pacman_background.get_height()

    # Create a graphical window by calling set_mode
    # Pygame represents images as Surface objects. The "display.set_mode()"
    # function creates a new Surface object that represents the actual
    # displayed graphics. Any drawing you do to this Surface will become
    # visible on the monitor.
    screen = pygame.display.set_mode(window_size)

    # Convert the pixel formats to that of the same type as our screen.
    ball = ball.convert_alpha() # Convert_alpha keeps the alpha channel in the pixel
    pacman_background = pacman_background.convert() # Removes alpha channel

    screen.blit(pacman_background,pacman_rect)
    while 1:
        # Detect the input and get a new direction
        # NOTE: This is the line that will be replaced by the agents once they are implemented
        direction = handle_input()

        # Fill the background that was erased by the ball
        screen.blit(pacman_background,ballrect,ballrect)

        # The class pygame.Rect is a rectanble represeting the position of the ball
        ballrect = ballrect.move(direction)

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

if __name__ == "__main__":
    main()