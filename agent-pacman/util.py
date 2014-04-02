__author__ = 'aortegag'

import os
import pygame

BLACK  = (   0,   0,   0)
WHITE  = ( 255, 255, 255)
BLUE   = (   0,   0, 255)
GREEN  = (   0, 255,   0)
RED    = ( 255,   0,   0)
PURPLE = ( 255,   0, 255)

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