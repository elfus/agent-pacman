__author__ = 'aortegag'

from characters import *
from collections import deque

OLD_DIRECTION = STAND_STILL
OLD_GOAL = 0
OLD_PATH = []

class WorldState:
    def __init__(self, pointsGroup):
        self.pacman_xy = Character.PACMAN.rect.center
        self.pacman_tile = Character.PACMAN.current_tile
        self.ghost_list = []
        for ghost in Character.GHOST_LIST:
            self.ghost_list.append((ghost.rect.center, ghost.current_tile))
        self.dots = pointsGroup
        self.game_mode = Character.CURRENT_MODE
        self.facing = Character.PACMAN.facing
        self.current_direction = Character.PACMAN.get_direction(self.facing)

    @staticmethod
    def getState(pointsGroup):
        return WorldState(pointsGroup)


def get_closest_pacman_point(state):
    """
    Gets the closest pacman point to pacman in terms of number of tiles in a path.

    This function makes a breadth-first search

    :param state:
    :return:
    """
    list_of_lists = []
    queue = deque([state.pacman_tile])
    expanded = []
    options_count = 0
    OPTIONS_LIMIT = 3
    while len(queue) > 0:
        current = queue.popleft()
        expanded.append(current)

        if current.point_exists:
            apath = [current] # In case current pacman point has a point
            while current.parent != 0 :
                current = current.parent
                apath.append(current)
            apath.reverse()
            list_of_lists.append(apath)
            options_count += 1
            # when there are a few dots cut the search when we find the first one
            if len(state.dots.sprites()) <= 25:
                break;
            # find up to OPTIONS_LIMIT dots
            if options_count == OPTIONS_LIMIT:
                break
            continue

        neighbors = get_tile_neighbors(Character.PACMAN.board_matrix, current)

        for n in neighbors:
            if n not in expanded:
                n.parent = current
                queue.append(n)

    for tile in expanded:
        tile.parent = 0

    list_of_lists = sorted(list_of_lists,key= lambda L:len(L))
    chosen_list = list_of_lists[0]
    # When we have two options with the same path cost (number of tiles to walk)
    # use a random index to have different games according to the system time
    random.seed()
    i = 0
    if len(list_of_lists) == 3:
        if len(list_of_lists[0]) == len(list_of_lists[1]) == len(list_of_lists[2]):
            i = random.randrange(3)
        if len(list_of_lists[0]) == len(list_of_lists[1]) != len(list_of_lists[2]):
            i = random.randrange(2)

    chosen_list = list_of_lists[i]
    Character.PACMAN.tile_list = chosen_list
    return chosen_list[-1], chosen_list

def get_direction_a_star(pointsGroup):
    """
    This function is the one that learns the game and determines which direction
    should pac man go.

    This algorithm can see and knows about the same things as a human player, i.e.
    the position of each ghost, the position of each point.

    The algorithm being used is A*
    :return:
    """
    global OLD_DIRECTION
    global OLD_GOAL
    global OLD_PATH
    Character.PACMAN.tile_list_options = []
    mState = WorldState.getState(pointsGroup)
    direction = STAND_STILL
    if OLD_GOAL.point_exists == False:
        OLD_GOAL, OLD_PATH = get_closest_pacman_point(mState)
    Character.PACMAN.goal_tile = OLD_GOAL

    if len(OLD_PATH) >= 2 and OLD_PATH[1] == mState.pacman_tile:
        OLD_PATH.pop(0)

    if len(OLD_PATH) == 1:
        direction = Character.PACMAN.get_closest_direction2(mState.pacman_tile,OLD_PATH[0])
    elif len(OLD_PATH) >= 2:
        direction = Character.PACMAN.get_closest_direction2(OLD_PATH[0],OLD_PATH[1])
        OLD_DIRECTION = direction

    if direction == STAND_STILL:
        direction = OLD_DIRECTION

    return direction


def reset_old_direction():
    global OLD_DIRECTION
    global OLD_GOAL
    global OLD_PATH
    OLD_DIRECTION = STAND_STILL
    OLD_PATH = []
    OLD_GOAL = Character.PACMAN.board_matrix[0][0]
