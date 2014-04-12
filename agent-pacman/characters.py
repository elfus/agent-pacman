from math import sqrt

__author__ = 'aortegag'

import pygame
from pygame.locals import *
from pygame.locals import *
from util import *

POINTS_LIST = 0

PACMAN_START = (105,206)
GHOST_START = (105,133)
BLINKY_START = (105, 108)

PACMAN = 0

INDEX_UP = 0
INDEX_RIGHT = 1
INDEX_DOWN = 2
INDEX_LEFT = 3

# OFFSET defined in util.py
DIRECTION_UP = [0, -OFFSET]
DIRECTION_RIGHT = [OFFSET, 0]
DIRECTION_DOWN = [0, OFFSET]
DIRECTION_LEFT = [-OFFSET, 0]

FACING_LEFT = "left"
FACING_RIGHT = "right"
FACING_UP = "up"
FACING_DOWN = "down"

SCATTER_MODE = 0 #"scatter"
FRIGHTENED_MODE = 1 #"frightened"
CHASE_MODE = 2 #"chase"
NUMBER_MODE = 3

class Character(pygame.sprite.Sprite):
    """A Ghost that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""
    PACMAN = 0
    BLINKY = 0
    CURRENT_MODE = CHASE_MODE

    def __init__(self, FILENAME, boardMatrix):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(FILENAME)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.stop()
        self.name = "Character"
        self.facing = FACING_LEFT
        self.tile_xy = (0,0)
        self.current_tile = 0
        self.board_matrix = boardMatrix
        self.scatter_tile = boardMatrix[0][0]
        print 'Character Constructor'

    def stop(self):
        self.movepos = [0, 0]
        self.state = "still"

    def get_opposite_direction(self, dir1):
        if dir1 == GO_LEFT: return GO_RIGHT
        if dir1 == GO_RIGHT: return GO_LEFT
        if dir1 == GO_UP: return GO_DOWN
        if dir1 == GO_DOWN: return GO_UP
        return STAND_STILL

    def get_direction(self, facing_to):
        if facing_to == FACING_LEFT: return GO_LEFT
        if facing_to == FACING_RIGHT: return GO_RIGHT
        if facing_to == FACING_DOWN: return GO_DOWN
        if facing_to == FACING_UP: return GO_UP

    def get_facing(self, direction):
        if direction == GO_LEFT: return FACING_LEFT
        if direction == GO_RIGHT: return FACING_RIGHT
        if direction == GO_DOWN: return FACING_DOWN
        if direction == GO_UP: return FACING_UP

    def detect_tunnel_condition(self):
        # This is if is meant to detect the case in which any character goes through
        # the 'middle tunnel' on the maze and appears on the other side
        if self.area.contains(self.rect) == False:
            if self.rect.left < (self.area.left - self.rect.width):
                self.rect.left = self.area.right
                return
            if self.rect.right > (self.area.right + self.rect.width):
                self.rect.right = self.area.left
                return

    def update(self):
        self.detect_tunnel_condition()
        if self.name != "Pacman":
            if Character.PACMAN.rect.collidepoint(self.rect.center):
                print "GAME OVER:",self.name,"killed Pacman"

    def get_adjacent_tile(self, facing_to):
        """
        Gets the adjacent tile to this character depending on where it is facing.
        This variable assumes the attribute variable self.facing is set before
        calling this method.

        :rtype : The tile (Rect) object adjacent where the character is facing
        :return: The tile coordinates in the board matrix
        """
        adjacent_tile = 0
        target_tile = (-1,-1)

        if facing_to == FACING_LEFT:
            target_tile = (self.tile_xy[0]-1,self.tile_xy[1])
        elif facing_to == FACING_RIGHT:
            target_tile = (self.tile_xy[0]+1,self.tile_xy[1])
        elif facing_to == FACING_UP:
            target_tile = (self.tile_xy[0],self.tile_xy[1]-1)
        elif facing_to == FACING_DOWN:
            target_tile = (self.tile_xy[0],self.tile_xy[1]+1)

        if target_tile[0] >= TILE_WIDTH_COUNT:
            target_tile = (0,target_tile[1])

        if target_tile[0] < 0:
            target_tile = (TILE_WIDTH_COUNT-1,target_tile[1])

        if target_tile[1] >= TILE_HEIGHT_COUNT:
            target_tile = (target_tile[0], 0)

        adjacent_tile = self.board_matrix[target_tile[0]][target_tile[1]]
        if adjacent_tile.isWalkable() == False:
            # print self.name,": the tile facing",facing_to,"is NOT walkable"
            if facing_to == FACING_LEFT or facing_to == FACING_RIGHT:
                if self.current_tile.rect.centerx != self.rect.centerx:
                    adjacent_tile = self.current_tile
                    target_tile = self.tile_xy
            elif facing_to == FACING_UP or facing_to == FACING_DOWN:
                if self.current_tile.rect.centery != self.rect.centery:
                    adjacent_tile = self.current_tile
                    target_tile = self.tile_xy

        return adjacent_tile, target_tile

    def movedirection(self, direction, pointsGroup):
        """

        :param direction: The direction the Character should go
        :param pointsGroup: A list of all the points that pacman can eat
        :return: True when the Character was able to move to the given direction, False otherwise
        """
        if self.can_move_to(direction) == False:
            return False

        new_facing = self.get_facing(direction)

        target_tile, target_xy = self.get_adjacent_tile(new_facing)

        self.facing = new_facing
        if target_tile.rect.collidepoint(self.rect.center) == True:
            self.current_tile = target_tile
            self.tile_xy = target_xy

        # Allow moving from left to right OR up and down
        if target_tile.rect.centery ==  self.rect.centery or target_tile.rect.centerx ==  self.rect.centerx:
            self.rect.move_ip(direction)

        if self.name == "Pacman":
            points_list = pygame.sprite.spritecollide(self,pointsGroup,True)
            for point in points_list:
                if point.is_energizer:
                    self.score += 5
                else:
                    self.score += 1
        return True

    def movedirection_in_ghost_house(self, direction, pointsGroup):
        """

        :param direction: The direction the Character should go
        :param pointsGroup: A list of all the points that pacman can eat
        :return: True when the Character was able to move to the given direction, False otherwise
        """
        new_facing = self.get_facing(direction)

        target_tile, target_xy = self.get_adjacent_tile(new_facing)

        self.facing = new_facing
        if target_tile.rect.centery == self.rect.centery:
            self.current_tile = target_tile
            self.tile_xy = target_xy
            return True # Strange bug

        self.rect.move_ip(direction) # Moves the image by 1 in y

        return True

    def get_direction_from_to(self,from_tile, to_tile):
        """
        Gets the direction needed to go from tile from_tile to tile to_tile
        :param from_tile: Source tile
        :param to_tile: Destiny tile
        :return: A direction
        """
        if from_tile.rect.centerx and to_tile.rect.centerx:
            if to_tile.rect.centerx < from_tile.rect.centerx:
                return GO_LEFT
            if to_tile.rect.centerx > from_tile.rect.centerx:
                return GO_RIGHT
        if from_tile.rect.centery and to_tile.rect.centery:
            if to_tile.rect.centery < from_tile.rect.centery:
                return GO_UP
            if to_tile.rect.centery > from_tile.rect.centery:
                return GO_DOWN
        return STAND_STILL

    def can_move_to(self,direction):
        """
        Tests wheather the Character can move to the given direction
        :param direction: The direction to test if we can move to
        :return: True if we can move, False otherwise
        """
        new_facing = self.get_facing(direction)
        target_tile, target_xy = self.get_adjacent_tile(new_facing)
        if target_tile.isWalkable() == False:
            return False
        if new_facing == FACING_UP or new_facing == FACING_DOWN:
            if target_tile.rect.centerx != self.rect.centerx:
                return False
        elif new_facing == FACING_LEFT or new_facing == FACING_RIGHT:
            if target_tile.rect.centery != self.rect.centery:
                return False
        return True

    def get_closest_direction(self, current_direction, from_tile, to_tile):
        """
        Gets the neighbors from tile from_tile, and then determines the closest tile to to_tile.
        :param from_tile:
        :param to_tile:
        """
        opposite_direction = self.get_opposite_direction(current_direction)
        back_facing = self.get_facing(opposite_direction)
        back_tile, back_tile_xy = self.get_adjacent_tile(back_facing)
        neighbors = get_tile_neighbors(self.board_matrix, from_tile)
        for tile in neighbors:
            if tile == self.current_tile:
                neighbors.remove(self.current_tile)
            if tile == back_tile:
                neighbors.remove(back_tile)
        d_list = []
        for tile in neighbors:
            distance = self.pitagorazo(tile.rect.centerx-to_tile.rect.centerx,
                                       tile.rect.centery-to_tile.rect.centery)
            d_list.append(distance)
        closest = min(d_list)
        index = d_list.index(closest)

        return self.get_direction_from_to(from_tile,neighbors[index])

    def pitagorazo(self, a, b):
        c = sqrt(pow(a,2) + pow(b,2))
        return c

    def __del__(self):
        print 'Destructor'

# Blinky is the red ghost
class Blinky(Character):
    def __init__(self, FILENAME, boardMatrix):
        Character.__init__(self, FILENAME, boardMatrix)
        self.name = "Blinky"
        # Every ghost needs the following three lines of code
        self.tile_xy = (13,14)
        self.current_tile = boardMatrix[self.tile_xy[0]][self.tile_xy[1]]
        self.rect.center = self.current_tile.getCenter()
        self.rect.centerx += 4
        self.current_direction = GO_LEFT
        self.last_kg_direction = STAND_STILL
        Character.BLINKY = self
        self.scatter_tile = boardMatrix[TILE_WIDTH_COUNT-4][0]
        print 'Blinky constructor'

    def update(self):
        global POINTS_LIST
        #Implement custom behavior, then call base class method
        target_tile = 0
        if Character.CURRENT_MODE == CHASE_MODE:
            target_tile = Character.PACMAN.current_tile
        elif Character.CURRENT_MODE == SCATTER_MODE:
            target_tile = self.scatter_tile
        elif Character.CURRENT_MODE == FRIGHTENED_MODE:
            target_tile = self.scatter_tile

        adjacent_tile, tile_xy = self.get_adjacent_tile(self.facing)
        # TODO: Add code to handle special intersections
        if adjacent_tile.is_intersection:
            self.current_direction = self.get_closest_direction(self.current_direction, adjacent_tile, target_tile)

        if self.movedirection(self.current_direction, POINTS_LIST) == True:
            self.last_kg_direction = self.current_direction
        else:
            if self.movedirection(self.last_kg_direction, POINTS_LIST) == False:
                self.current_direction = self.get_closest_direction(self.last_kg_direction,self.current_tile, target_tile)

        Character.update(self)

    def __del__(self):
        print 'Blinky destructor'

# Pinky is the pink ghost
class Pinky(Character):
    def __init__(self, FILENAME, boardMatrix):
        Character.__init__(self, FILENAME, boardMatrix)
        self.name = "Pinky"
        # Every ghost needs the following three lines of code
        self.tile_xy = (13,17)
        self.current_tile = boardMatrix[self.tile_xy[0]][self.tile_xy[1]]
        self.rect.center = self.current_tile.getCenter()
        self.rect.centerx += 4
        self.current_direction = GO_LEFT
        self.last_kg_direction = STAND_STILL
        self.scatter_tile = boardMatrix[3][0]
        print 'Pinky constructor'

    def update(self):
        #Implement custom behavior, then call base class method
        if self.current_tile.is_in_ghost_house:
            if self.pinky_exits_ghost_house() == False:
                print self.name, "ERROR: Could not exit ghost house"
            Character.update(self)
            return

        target_tile = 0
        if Character.CURRENT_MODE == CHASE_MODE:
            pacman_tile = Character.PACMAN.current_tile
            pacman_facing = Character.PACMAN.facing
            target_tile = self.get_pinky_target(pacman_facing, pacman_tile)
        elif Character.CURRENT_MODE == SCATTER_MODE:
            target_tile = self.scatter_tile
        elif Character.CURRENT_MODE == FRIGHTENED_MODE:
            target_tile = self.scatter_tile

        adjacent_tile, tile_xy = self.get_adjacent_tile(self.facing)
        # TODO: Add code to handle special intersections
        if adjacent_tile.is_intersection:
            self.current_direction = self.get_closest_direction(self.current_direction, adjacent_tile, target_tile)

        if self.movedirection(self.current_direction, POINTS_LIST) == True:
            self.last_kg_direction = self.current_direction
        else:
            if self.movedirection(self.last_kg_direction, POINTS_LIST) == False:
                self.current_direction = self.get_closest_direction(self.last_kg_direction, self.current_tile, target_tile)

        Character.update(self)

    def pinky_exits_ghost_house(self):
        global POINTS_LIST
        return self.movedirection_in_ghost_house(GO_UP,POINTS_LIST)

    def get_pinky_target(self, pacman_facing, pacman_tile):
        target = 0
        if pacman_facing == FACING_LEFT:
            x,y = pacman_tile.board_coordinate[0]-4, pacman_tile.board_coordinate[1]
        elif pacman_facing == FACING_RIGHT:
            x,y = pacman_tile.board_coordinate[0]+4, pacman_tile.board_coordinate[1]
        elif pacman_facing == FACING_DOWN:
            x,y = pacman_tile.board_coordinate[0], pacman_tile.board_coordinate[1]+4
        elif pacman_facing == FACING_UP:
            x,y = pacman_tile.board_coordinate[0]-4, pacman_tile.board_coordinate[1]-4

        if x < 0: x = 0
        if y < 0: y = 0
        if x >= TILE_WIDTH_COUNT: x = TILE_WIDTH_COUNT-1
        if y >= TILE_HEIGHT_COUNT: y = TILE_HEIGHT_COUNT-1

        target = self.board_matrix[x][y];

        return target

    def __del__(self):
        print 'Pink destructor'

# Inky is the cyan ghost
class Inky(Character):
    def __init__(self, FILENAME,boardMatrix):
        Character.__init__(self, FILENAME,boardMatrix)
        self.name = "Inky"
         # Every ghost needs the following three lines of code
        self.tile_xy = (11,17)
        self.current_tile = boardMatrix[self.tile_xy[0]][self.tile_xy[1]]
        self.rect.center = self.current_tile.getCenter()
        self.rect.centerx += 4
        self.current_direction = GO_LEFT
        self.last_kg_direction = STAND_STILL
        self.scatter_tile = boardMatrix[TILE_WIDTH_COUNT-1][TILE_HEIGHT_COUNT-1]
        print 'Inky constructor'

    def update(self):
        #Implement custom behavior, then call base class method
        if self.current_tile.is_in_ghost_house and Character.PACMAN.score >=30:
            if self.inky_exits_ghost_house() == False:
                print self.name, "ERROR: Could not exit ghost house"
            Character.update(self)
            return

        if Character.PACMAN.score < 30:
            return

        target_tile = 0
        if Character.CURRENT_MODE == CHASE_MODE:
            # TODO Change this behavior specific to inky
            pacman_tile = Character.PACMAN.current_tile
            pacman_facing = Character.PACMAN.facing
            blinky_tile = Character.BLINKY.current_tile # tuple
            target_tile = self.get_inky_target(pacman_facing, pacman_tile, blinky_tile)
        elif Character.CURRENT_MODE == SCATTER_MODE:
            target_tile = self.scatter_tile
        elif Character.CURRENT_MODE == FRIGHTENED_MODE:
            target_tile = self.scatter_tile

        adjacent_tile, tile_xy = self.get_adjacent_tile(self.facing)
        # TODO: Add code to handle special intersections
        if adjacent_tile.is_intersection:
            self.current_direction = self.get_closest_direction(self.last_kg_direction, adjacent_tile, target_tile)

        if self.movedirection(self.current_direction, POINTS_LIST) == True:
            self.last_kg_direction = self.current_direction
        else:
            if self.movedirection(self.last_kg_direction, POINTS_LIST) == False:
                self.current_direction = self.get_closest_direction(self.last_kg_direction, self.current_tile, target_tile)

        Character.update(self)

    def get_inky_target(self, pacman_facing, pacman_tile, blinky_tile):
        target = 0
        if pacman_facing == FACING_LEFT:
            x,y = pacman_tile.board_coordinate[0]-2, pacman_tile.board_coordinate[1]
        elif pacman_facing == FACING_RIGHT:
            x,y = pacman_tile.board_coordinate[0]+2, pacman_tile.board_coordinate[1]
        elif pacman_facing == FACING_DOWN:
            x,y = pacman_tile.board_coordinate[0], pacman_tile.board_coordinate[1]+2
        elif pacman_facing == FACING_UP:
            x,y = pacman_tile.board_coordinate[0]-2, pacman_tile.board_coordinate[1]-2

        if x < 0: x = 0
        if y < 0: y = 0
        if x >= TILE_WIDTH_COUNT: x = TILE_WIDTH_COUNT-1
        if y >= TILE_HEIGHT_COUNT: y = TILE_HEIGHT_COUNT-1

        # Use blinky's position
        target = self.board_matrix[x][y];
        c1 = self.pitagorazo(target.rect.centerx - blinky_tile.rect.centerx, target.rect.centery - blinky_tile.rect.centery)

        x2 = (abs(x - blinky_tile.board_coordinate[0]) * 2) + blinky_tile.board_coordinate[0]
        y2 = (abs(y - blinky_tile.board_coordinate[1]) * 2) + blinky_tile.board_coordinate[1]

        if x2 < 0: x = 0
        if y2 < 0: y = 0
        if x2 >= TILE_WIDTH_COUNT: x2 = TILE_WIDTH_COUNT-1
        if y2 >= TILE_HEIGHT_COUNT: y2 = TILE_HEIGHT_COUNT-1
        real_target = self.board_matrix[x2][y2]
        # This piece of code was just to validate the calculations were right
        # c2 = self.pitagorazo(real_target.rect.centerx - blinky_tile.rect.centerx, real_target.rect.centery - blinky_tile.rect.centery)
        # if (c1*2) == c2:
        #     print "SUCCESS"
        # else:
        #     print "FAILURE"

        return real_target

    def inky_exits_ghost_house(self):
        global POINTS_LIST
        exit_tile = self.board_matrix[13][14]
        if self.rect.centerx < exit_tile.rect.right:
            new_facing = self.get_facing(GO_RIGHT)

            target_tile, target_xy = self.get_adjacent_tile(new_facing)

            self.facing = new_facing
            if target_tile.rect.right == self.rect.centerx:
                self.current_tile = self.board_matrix[13][17]
                self.tile_xy = (13,17)
                return True # Strange bug

            self.rect.move_ip(GO_RIGHT) # Moves the image by 1 in y
            return True

        if self.rect.centerx == exit_tile.rect.right:
            if self.rect.centery > exit_tile.rect.centery:
                new_facing = self.get_facing(GO_UP)

                target_tile, target_xy = self.get_adjacent_tile(new_facing)

                self.facing = new_facing
                if target_tile.rect.centery == self.rect.centery:
                    self.current_tile = target_tile
                    self.tile_xy = target_xy
                    return True # Strange bug

                self.rect.move_ip(GO_UP) # Moves the image by 1 in y
                return True

            if self.rect.centery == exit_tile.rect.centery:
                self.current_tile = self.board_matrix[13][14]
                self.tile_xy = (13,14)

    def __del__(self):
        print 'Inky destructor'

# Clyde is the orange ghost
class Clyde(Character):
    def __init__(self, FILENAME,boardMatrix):
        Character.__init__(self, FILENAME,boardMatrix)
        self.name = "Clyde"
         # Every ghost needs the following three lines of code
        self.tile_xy = (15,17)
        self.current_tile = boardMatrix[self.tile_xy[0]][self.tile_xy[1]]
        self.rect.center = self.current_tile.getCenter()
        self.rect.centerx += 4
        self.current_direction = GO_LEFT
        self.last_kg_direction = 0
        self.scatter_tile = boardMatrix[0][TILE_HEIGHT_COUNT-1]
        print 'Clyde constructor'

    def update(self):
        #Implement custom behavior, then call base class method
        if self.current_tile.is_in_ghost_house and Character.PACMAN.score >=50:
            if self.clyde_exits_ghost_house() == False:
                print self.name, "ERROR: Could not exit ghost house"
            Character.update(self)
            return

        if Character.PACMAN.score < 50:
            return

        target_tile = 0
        if Character.CURRENT_MODE == CHASE_MODE:
            #TODO Change this behavior specific to clyde
            ref_tile = self.board_matrix[self.tile_xy[0]][self.tile_xy[1]-7]
            radius = self.pitagorazo(self.rect.centerx - ref_tile.rect.centerx, self.rect.centery - ref_tile.rect.centery)
            pacman_tile = Character.PACMAN.current_tile
            distance = self.pitagorazo(self.rect.centerx - pacman_tile.rect.centerx, self.rect.centery - pacman_tile.rect.centery)
            if distance <= radius: # when pacman is close go to scatter tile
                target_tile =self.scatter_tile
            else: # when pacman is far imitate blinky's behavior
                target_tile = pacman_tile
        elif Character.CURRENT_MODE == SCATTER_MODE:
            target_tile = self.scatter_tile
        elif Character.CURRENT_MODE == FRIGHTENED_MODE:
            target_tile = self.scatter_tile

        adjacent_tile, tile_xy = self.get_adjacent_tile(self.facing)
        # TODO: Add code to handle special intersections
        if adjacent_tile.is_intersection:
            self.current_direction = self.get_closest_direction(self.last_kg_direction, adjacent_tile, target_tile)

        if self.movedirection(self.current_direction, POINTS_LIST) == True:
            self.last_kg_direction = self.current_direction
        else:
            if self.movedirection(self.last_kg_direction, POINTS_LIST) == False:
                self.current_direction = self.get_closest_direction(self.last_kg_direction, self.current_tile, target_tile)

        Character.update(self)

    def clyde_exits_ghost_house(self):
        global POINTS_LIST
        exit_tile = self.board_matrix[13][14]
        if self.rect.centerx > exit_tile.rect.right:
            new_facing = self.get_facing(GO_LEFT)

            target_tile, target_xy = self.get_adjacent_tile(new_facing)

            self.facing = new_facing
            if target_tile.rect.left == self.rect.centerx:
                self.current_tile = self.board_matrix[13][17]
                self.tile_xy = (13,17)
                return True # Strange bug

            self.rect.move_ip(GO_LEFT) # Moves the image by 1 in y
            return True

        if self.rect.centerx == exit_tile.rect.right:
            if self.rect.centery > exit_tile.rect.centery:
                new_facing = self.get_facing(GO_UP)

                target_tile, target_xy = self.get_adjacent_tile(new_facing)

                self.facing = new_facing
                if target_tile.rect.centery == self.rect.centery:
                    self.current_tile = target_tile
                    self.tile_xy = target_xy
                    return True # Strange bug

                self.rect.move_ip(GO_UP) # Moves the image by 1 in y
                return True

            if self.rect.centery == exit_tile.rect.centery:
                self.current_tile = self.board_matrix[13][14]
                self.tile_xy = (13,14)


    def __del__(self):
        print 'Clyde destructor'

# Pacman is pacman
class Pacman(Character):
    def __init__(self, FILENAME, boardMatrix):
        Character.__init__(self, FILENAME, boardMatrix)
        self.name = "Pacman"
        self.score = 0
        self.tile_xy = (13,26)
        self.current_tile = boardMatrix[self.tile_xy[0]][self.tile_xy[1]]
        self.rect.center = self.current_tile.getCenter()
        Character.PACMAN = self
        print 'Pacman constructor'

    def update(self):
        #Implement custom behavior, then call base class method
        Character.update(self)

    def __del__(self):
        print 'Pacman destructor'

def get_characters_group(boardMatrix, pointsGroup):
    global PACMAN
    global POINTS_LIST

    POINTS_LIST = pointsGroup

    PACMAN = pacman = Pacman("pacman1.png", boardMatrix)

    blinky = Blinky("rojo.png", boardMatrix)
    pinky = Pinky("rosa.png", boardMatrix)
    clyde = Clyde("naranja.png",boardMatrix)
    inky = Inky("azulito.png",boardMatrix)


    ghostsprite = pygame.sprite.RenderPlain()
    ghostsprite.add(blinky)
    ghostsprite.add(pinky)
    ghostsprite.add(inky)
    ghostsprite.add(clyde)
    ghostsprite.add(pacman)
    return ghostsprite, pacman
