from math import sqrt

__author__ = 'aortegag'

import pygame
from pygame.locals import *
from pygame.locals import *
from util import *
import random
import time

POINTS_LIST = 0

PACMAN_START = (105,206)
GHOST_START = (105,133)
BLINKY_START = (105, 108)

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

BLINKY_ID = 0
PINKY_ID = 1
INKY_ID = 2
CLYDE_ID = 3

MODE_STR = ["Scatter","Frightened","Chase"]

def next_mode():
    old_mode = MODE_STR[Character.CURRENT_MODE]
    Character.CURRENT_MODE = (Character.CURRENT_MODE+1) % NUMBER_MODE
    print "Game mode changed from",old_mode," to",MODE_STR[Character.CURRENT_MODE]
    return

def change_mode(new_mode):
    old_mode = MODE_STR[Character.CURRENT_MODE]
    if new_mode == Character.CURRENT_MODE:
        print "Current mode ", old_mode
        return
    if new_mode < SCATTER_MODE or new_mode > CHASE_MODE:
        print "INVALID MODE, keeping current mode: ",old_mode
        return
    Character.CURRENT_MODE = new_mode
    print "Game mode changed from",old_mode," to",MODE_STR[Character.CURRENT_MODE]
    return

class Character(pygame.sprite.Sprite):
    """A Ghost that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""
    PACMAN = 0
    BLINKY = 0
    GHOST_LIST = [0, 0, 0, 0] # List for 4 ghosts
    CURRENT_MODE = CHASE_MODE
    GAME_OVER = False
    CHANGE_TO_FRIGHTENED = False

    def __init__(self, FILENAME, boardMatrix):
        pygame.sprite.Sprite.__init__(self)
        self.normal_image, self.normal_rect = load_image(FILENAME)
        self.frightened_image, self.frightened_rect = load_image("asustado.png")
        self.image, self.rect = self.normal_image, self.normal_rect
        screen = pygame.display.get_surface()
        self.board_area = screen.get_rect()
        self.board_rect = pygame.Rect(0,0,BOARD_WIDTH,BOARD_HEIGHT)
        self.name = "Character"
        self.reset_state(boardMatrix)
        self.killed = False
        self.waiting = False
        self.TIME_IN_GHOST_HOUSE = 0
        print 'Character Constructor'

    def reset_state(self, boardMatrix):
        self.stop()
        self.facing = FACING_LEFT
        self.tile_xy = (0,0)
        self.current_tile = 0
        self.board_matrix = boardMatrix
        self.scatter_tile = boardMatrix[0][0]
        self.frightened_counter = 0
        self.frightened_tile = self.get_random_tile()
        self.initial_position = (0,0)

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
        if self.board_rect.contains(self.rect) == False:
            if self.rect.left < (0 - self.rect.width):
                self.rect.left = BOARD_WIDTH
                return
            if self.rect.right > (BOARD_WIDTH + self.rect.width):
                self.rect.right = 0
                return

    def update(self):
        self.detect_tunnel_condition()
        # This is where we detect collisions between pacman and the ghosts
        if self.name != "Pacman":
            if Character.CURRENT_MODE == FRIGHTENED_MODE:
                self.image = self.frightened_image
            else:
                self.image = self.normal_image
                
            if Character.PACMAN.rect.collidepoint(self.rect.center):
                if Character.CURRENT_MODE == CHASE_MODE or Character.CURRENT_MODE == SCATTER_MODE:
                    print "GAME OVER:",self.name,"killed Pacman"
                    # Reset world state
                    Character.PACMAN.reset_state(self.board_matrix)
                    for ghost in Character.GHOST_LIST:
                        ghost.reset_state(self.board_matrix)
                    Character.GAME_OVER = True
                elif Character.CURRENT_MODE == FRIGHTENED_MODE:
                    print "PACMAN just killed",self.name
                    self.killed = True

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

    def move_to_tile(self, target_tile):
        adjacent_tile, tile_xy = self.get_adjacent_tile(self.facing)
        # TODO: Add code to handle special intersections
        if adjacent_tile.is_intersection:
            self.current_direction = self.get_closest_direction(self.current_direction, adjacent_tile, target_tile)

        if self.movedirection(self.current_direction, POINTS_LIST) == True:
            self.last_kg_direction = self.current_direction
        else:
            if self.movedirection(self.last_kg_direction, POINTS_LIST) == False:
                self.current_direction = self.get_closest_direction(self.last_kg_direction,self.current_tile, target_tile)

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
                    Character.CHANGE_TO_FRIGHTENED = True
                else:
                    self.score += 1
            if self.score > self.highest_score:
                self.highest_score = self.score
        return True

    def movedirection_in_ghost_house(self, direction, pointsGroup):
        """

        :param direction: The direction the Character should go
        :param pointsGroup: A list of all the points that pacman can eat
        :return: True when the Character was able to move to the given direction, False otherwise
        """
        new_facing = self.get_facing(direction)
        exit_tile = self.board_matrix[13][14]

        self.facing = new_facing
        if exit_tile.rect.centery == self.rect.centery:
            self.current_tile = exit_tile
            self.tile_xy = (13,14)
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

    def get_random_tile(self):
        x = random.randrange(0, TILE_WIDTH_COUNT-1)
        y = 2
        if self.name == "Inky" or self.name == "Clyde":
            if self.frightened_counter <= 10:
                y = random.randrange(0, 2)
            else:
                y = random.randrange(TILE_HEIGHT_COUNT-3, TILE_HEIGHT_COUNT-1)
        elif self.name == "Blinky" or self.name == "Pinky":
            if self.frightened_counter <= 10:
                y = random.randrange(TILE_HEIGHT_COUNT-3, TILE_HEIGHT_COUNT-1)
            else:
                y = random.randrange(0, 2)
        self.frightened_counter += 1
        if self.frightened_counter == 21:
            self.frightened_counter = 0
        return self.board_matrix[x][y]

    def pitagorazo(self, a, b):
        c = sqrt(pow(a,2) + pow(b,2))
        return c

    def ghost_goes_back_home(self):
        enter_tile1 = self.board_matrix[13][14]
        enter_tile2 = self.board_matrix[14][14]
        center_ghost_house = self.board_matrix[13][17]
        enter_center = (enter_tile1.rect.right, enter_tile1.rect.centery)
        # Position right above the ghost house
        if self.current_tile.is_in_ghost_house == False:
            # Arriving from the left
            if self.rect.centerx < enter_center[0]:
                self.move_to_tile(enter_tile1)
                return True
            # Arriving from the right
            elif self.rect.centerx > enter_center[0]:
                self.move_to_tile(enter_tile2)
                return True

            #This will move us into a tile that is inside the ghost house
            if self.rect.centerx == enter_tile1.rect.right:
                if self.rect.centery < self.ghost_tile.rect.centery:
                    self.rect.move_ip(GO_DOWN)
                    return True

            self.current_tile = center_ghost_house
            self.tile_xy = (13,17)


        # We are in the center of the house, move each ghost to their respective side
        if self.rect.centery == self.ghost_tile.rect.centery:
            # Move to the desired side
            if self.rect.centerx != self.initial_position[0]:
                self.rect.move_ip(self.get_direction_from_to(center_ghost_house,self.ghost_tile))
                return True
            # We are positioned on the side we want
            if self.rect.centerx == self.initial_position[0]:
                self.current_tile = self.ghost_tile
                self.tile_xy = self.ghost_tile_xy
                self.TIME_IN_GHOST_HOUSE = time.time()
                self.killed = False
                self.waiting = True
        return True

    def pinky_exits_ghost_house(self):
        global POINTS_LIST
        return self.movedirection_in_ghost_house(GO_UP,POINTS_LIST)

    def __del__(self):
        print 'Destructor'

# Blinky is the red ghost
class Blinky(Character):
    def __init__(self, FILENAME, boardMatrix):
        Character.__init__(self, FILENAME, boardMatrix)
        self.name = "Blinky"
        self.reset_state(boardMatrix)
        Character.BLINKY = self
        Character.GHOST_LIST[BLINKY_ID] = self
        print 'Blinky constructor'

    def reset_state(self, boardMatrix):
        # Every ghost needs the following three lines of code
        Character.reset_state(self,boardMatrix)
        self.tile_xy = (13,14)
        self.current_tile = boardMatrix[self.tile_xy[0]][self.tile_xy[1]]
        self.ghost_tile_xy = (11,17)
        self.ghost_tile = boardMatrix[self.ghost_tile_xy[0]][self.ghost_tile_xy[1]]
        self.rect.center = self.current_tile.getCenter()
        self.rect.centerx += 4
        self.initial_position = (self.rect.centerx, self.rect.centery)
        self.current_direction = GO_LEFT
        self.last_kg_direction = STAND_STILL
        self.scatter_tile = boardMatrix[TILE_WIDTH_COUNT-4][0]


    def update(self):
        global POINTS_LIST
        if self.killed == True:
            if self.ghost_goes_back_home() == False:
                print self.name, "ERROR: Could not go back home"
            return

        if self.current_tile.is_in_ghost_house:
            if self.waiting == True:
                ENDED = time.time()
                time_elapsed = ENDED - self.TIME_IN_GHOST_HOUSE
                if time_elapsed > 3:
                    self.waiting = False
                return
            if self.pinky_exits_ghost_house() == False:
                print self.name, "ERROR: Could not exit ghost house"
            Character.update(self)
            return

        target_tile = 0
        if Character.CURRENT_MODE == CHASE_MODE:
            target_tile = Character.PACMAN.current_tile
        elif Character.CURRENT_MODE == SCATTER_MODE:
            target_tile = self.scatter_tile
        elif Character.CURRENT_MODE == FRIGHTENED_MODE:
            target_tile = self.frightened_tile
            if self.current_tile.is_intersection and self.current_tile.rect.center == self.rect.center:
                target_tile = self.frightened_tile = self.get_random_tile()

        self.move_to_tile(target_tile)

        Character.update(self)

    def __del__(self):
        print 'Blinky destructor'

# Pinky is the pink ghost
class Pinky(Character):
    def __init__(self, FILENAME, boardMatrix):
        Character.__init__(self, FILENAME, boardMatrix)
        self.name = "Pinky"
        self.reset_state(boardMatrix)
        Character.GHOST_LIST[PINKY_ID] = self
        print 'Pinky constructor'

    def reset_state(self, boardMatrix):
        Character.reset_state(self,boardMatrix)
        # Every ghost needs the following three lines of code
        self.tile_xy = (13,17)
        self.current_tile = boardMatrix[self.tile_xy[0]][self.tile_xy[1]]
        self.ghost_tile_xy = (13,17)
        self.ghost_tile = boardMatrix[self.ghost_tile_xy[0]][self.ghost_tile_xy[1]]
        self.rect.center = self.current_tile.getCenter()
        self.rect.centerx += 4
        self.initial_position = (self.rect.centerx, self.rect.centery)
        self.current_direction = GO_LEFT
        self.last_kg_direction = STAND_STILL
        self.scatter_tile = boardMatrix[3][0]

    def update(self):
        if self.killed == True:
            if self.ghost_goes_back_home() == False:
                print self.name, "ERROR: Could not go back home"
            return

        if self.current_tile.is_in_ghost_house:
            if self.waiting == True:
                ENDED = time.time()
                time_elapsed = ENDED - self.TIME_IN_GHOST_HOUSE
                if time_elapsed > 3:
                    self.waiting = False
                return
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
            target_tile = self.frightened_tile
            if self.current_tile.is_intersection and self.current_tile.rect.center == self.rect.center:
                target_tile = self.frightened_tile = self.get_random_tile()

        self.move_to_tile(target_tile)

        Character.update(self)

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
        self.reset_state(boardMatrix)
        Character.GHOST_LIST[INKY_ID] = self
        print 'Inky constructor'

    def reset_state(self, boardMatrix):
        Character.reset_state(self,boardMatrix)
         # Every ghost needs the following three lines of code
        self.tile_xy = (11,17)
        self.current_tile = boardMatrix[self.tile_xy[0]][self.tile_xy[1]]
        self.ghost_tile_xy = (11,17)
        self.ghost_tile = boardMatrix[self.ghost_tile_xy[0]][self.ghost_tile_xy[1]]
        self.rect.center = self.current_tile.getCenter()
        self.rect.centerx += 4
        self.initial_position = (self.rect.centerx, self.rect.centery)
        self.current_direction = GO_LEFT
        self.last_kg_direction = STAND_STILL
        self.scatter_tile = boardMatrix[TILE_WIDTH_COUNT-1][TILE_HEIGHT_COUNT-1]

    def update(self):
        if self.killed == True:
            if self.ghost_goes_back_home() == False:
                print self.name, "ERROR: Could not go back home"
            return

        #Implement custom behavior, then call base class method
        if self.current_tile.is_in_ghost_house and Character.PACMAN.score >=30:
            if self.waiting == True:
                ENDED = time.time()
                time_elapsed = ENDED - self.TIME_IN_GHOST_HOUSE
                if time_elapsed > 3:
                    self.waiting = False
                return
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
            target_tile = self.frightened_tile
            if self.current_tile.is_intersection and self.current_tile.rect.center == self.rect.center:
                target_tile = self.frightened_tile = self.get_random_tile()

        self.move_to_tile(target_tile)

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
        self.reset_state(boardMatrix)
        Character.GHOST_LIST[CLYDE_ID] = self
        print 'Clyde constructor'

    def reset_state(self, boardMatrix):
        Character.reset_state(self,boardMatrix)
         # Every ghost needs the following three lines of code
        self.tile_xy = (15,17)
        self.current_tile = boardMatrix[self.tile_xy[0]][self.tile_xy[1]]
        self.ghost_tile_xy = (15,17)
        self.ghost_tile = boardMatrix[self.ghost_tile_xy[0]][self.ghost_tile_xy[1]]
        self.rect.center = self.current_tile.getCenter()
        self.rect.centerx += 4
        self.initial_position = (self.rect.centerx, self.rect.centery)
        self.current_direction = GO_LEFT
        self.last_kg_direction = 0
        self.scatter_tile = boardMatrix[0][TILE_HEIGHT_COUNT-1]

    def update(self):
        if self.killed == True:
            if self.ghost_goes_back_home() == False:
                print self.name, "ERROR: Could not go back home"
            return

        if self.current_tile.is_in_ghost_house and Character.PACMAN.score >=50:
            if self.waiting == True:
                ENDED = time.time()
                time_elapsed = ENDED - self.TIME_IN_GHOST_HOUSE
                if time_elapsed > 3:
                    self.waiting = False
                return
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
            target_tile = self.frightened_tile
            if self.current_tile.is_intersection and self.current_tile.rect.center == self.rect.center:
                target_tile = self.frightened_tile = self.get_random_tile()

        self.move_to_tile(target_tile)

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
        Character.PACMAN = self
        self.highest_score = 0
        self.reset_state(boardMatrix)
        print 'Pacman constructor'

    def reset_state(self, boardMatrix):
        Character.reset_state(self,boardMatrix)
        self.score = 0
        self.tile_xy = (13,26)
        self.current_tile = boardMatrix[self.tile_xy[0]][self.tile_xy[1]]
        self.rect.center = self.current_tile.getCenter()

    def update(self):
        #Implement custom behavior, then call base class method
        Character.update(self)

    def __del__(self):
        print 'Pacman destructor'

def get_characters_group(boardMatrix, pointsGroup):
    global POINTS_LIST

    POINTS_LIST = pointsGroup

    pacman = Pacman("pacman1.png", boardMatrix)

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
