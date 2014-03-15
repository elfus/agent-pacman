#! /usr/bin/python
__author__ = 'aortegag'

import sys, pygame

def main():
    pygame.init()
    size = width, height = 320, 240
    speed = [2, 2]
    black = 0, 0, 0

    # Create a graphical window by calling set_mode
    # Pygame represents images as Surface objects. The "display.set_mode()"
    # function creates a new Surface object that represents the actual
    # displayed graphics. Any drawing you do to this Surface will become
    # visible on the monitor.
    screen = pygame.display.set_mode(size)
    ball = pygame.image.load("ball.gif")
    ballrect = ball.get_rect()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            ballrect = ballrect.move(speed)
            if ballrect.left < 0 or ballrect.right > width:
                speed[0] = -speed[0]
            if ballrect.top < 0 or ballrect.bottom > height:
                speed[1] = -speed[1]

            #Erase the the screen by filling it with a black RGB color
            screen.fill(black)

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