__author__ = 'aortegag'

from characters import *
from collections import deque

OLD_DIRECTION = STAND_STILL


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


def getPossibleActions():
    possible_actions = []
    if Character.PACMAN.can_move_to(GO_LEFT):
        possible_actions.append(GO_LEFT)
    if Character.PACMAN.can_move_to(GO_RIGHT):
        possible_actions.append(GO_RIGHT)
    if Character.PACMAN.can_move_to(GO_DOWN):
        possible_actions.append(GO_DOWN)
    if Character.PACMAN.can_move_to(GO_UP):
        possible_actions.append(GO_UP)
    return possible_actions


def next_direction(direction):
    if direction == GO_LEFT:
        return GO_UP
    if direction == GO_UP:
        return GO_RIGHT
    if direction == GO_RIGHT:
        return GO_DOWN
    if direction == GO_DOWN:
        return GO_LEFT


def find_pacman_points(current_tile, last_tile):
    """
    This function recursively finds the closest point to the current_tile
    :param current_tile: Current tile where we are now
    :param last_tile: The last tile we visited.
    :return: A list of tiles representing the path.
    """
    tile_list = []
    if current_tile.visited == True:
        return tile_list

    current_tile.visited = True

    if current_tile.point_exists == True:
        tile_list.append([current_tile])
        current_tile.visited = False
        return tile_list

    neighbors = get_tile_neighbors(Character.PACMAN.board_matrix, current_tile)

    for tile in neighbors:
        if tile == last_tile:
            continue
        sublist = []
        sublist.append(current_tile)
        if tile.visited == False:
            tile_eaten = find_pacman_points(tile, current_tile)
            sublist.extend(tile_eaten[-1])
        tile_list.append(sublist)


    # handle the tunnel condition
    if len(tile_list) == 0:
        if current_tile.board_coordinate == (0, 17):
            sublist = []
            sublist.append(current_tile)
            new_tile = Character.PACMAN.board_matrix[TILE_WIDTH_COUNT - 1][17]
            tile_eaten = find_pacman_points(new_tile, current_tile)
            sublist.extend(tile_eaten[-1])
            tile_list.append(sublist)
        elif current_tile.board_coordinate == (TILE_WIDTH_COUNT - 1, 17):
            sublist = []
            sublist.append(current_tile)
            new_tile = Character.PACMAN.board_matrix[0][17]
            tile_eaten = find_pacman_points(new_tile, current_tile)
            sublist.extend(tile_eaten[-1])
            tile_list.append(sublist)

    current_tile.visited = False
    return tile_list

def find_closest_pacman_point(state):
    h_list = []
    for dot in state.dots:
        px = Character.PACMAN.rect.x
        py = Character.PACMAN.rect.y
        tx = dot.rect.x
        ty = dot.rect.y
        h = Character.PACMAN.pitagorazo(px-tx, py-ty)
        h_list.append((h,dot))
    h_list = sorted(h_list,key=lambda item:item[0])
    return h_list[0][1]

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
    while len(queue) > 0:
        current = queue.popleft()
        current.visited = True

        if current.point_exists:
            apath = [current] # In case current pacman point has a point
            while current.parent != 0 :
                current = current.parent
                apath.append(current)
            list_of_lists.append(apath)
            continue

        neighbors = get_tile_neighbors(Character.PACMAN.board_matrix, current)
        expanded.append(current)

        for n in neighbors:
            if n not in expanded:
                n.parent = current
                queue.append(n)


    for sublist in list_of_lists:
        for tile in sublist:
            tile.parent = 0
            tile.visited = False

    Character.PACMAN.tile_list = list_of_lists[0]
    return list_of_lists[0][0]


def g(state, action):
    """
    The g() function returns the cost from the initial node to the actual position

    TODO: Implement :)

    :param state: Current World state
    :param action: The action we want to take
    :return:
    """
    return 0

def is_going_away_from_goal(current_tile, goal_tile, direction):
    """
    This function checks the special case in which the current_tile is neighbor from the goal_tile
    but the current direction about to be applied makes pacman go away from the goal_tile
    :param current_tile:
    :param goal_tile:
    :param direction:
    :return: True when direction makes pacman go away from goal_tile when it's a neighbor
    """
    neighbors = get_tile_neighbors(Character.PACMAN.board_matrix, current_tile)
    for tile in neighbors:
        if tile == goal_tile:
            real_direction = Character.PACMAN.get_direction_from_to(current_tile, goal_tile)
            if real_direction != direction:
                return True
    return False


def find_path(current_tile, last_tile, goal_tile, direction):
    """
    Finds a path from the current_tile to the goal_tile using the given direction and making sure
    we don't go back through the last_tile.

    :param current_tile:
    :param last_tile:
    :param goal_tile:
    :param direction:
    :return:
    """
    tile_list = []
    if current_tile.visited == True:
        return -1

    current_tile.visited = True

    if current_tile == goal_tile:
        tile_list.append(current_tile)
        current_tile.visited = False
        return tile_list

    if current_tile.is_in_ghost_house == True:
        current_tile.visited = False
        return tile_list

    if is_going_away_from_goal(current_tile,goal_tile,direction) == True:
        current_tile.visited = False
        return -1

    facing_to = Character.PACMAN.get_facing(direction)
    adjacent_tile, tile_xy = Character.PACMAN.get_adjacent_tile_to(current_tile, facing_to)
    if adjacent_tile.is_walkable == False:
        current_tile.visited = False
        return -1
    tile_list.append(current_tile)
    direction = Character.PACMAN.get_closest_direction_excluding(direction, adjacent_tile, goal_tile, tile_list)
    subpath = find_path(adjacent_tile, current_tile, goal_tile, direction)
    if isinstance(subpath, list):
        tile_list.extend(subpath)
    if isinstance(subpath, int):
        if subpath == -1:
            tile_list = -1
    current_tile.visited = False
    return tile_list


def h(state, direction, goal_tile):
    """
    The h() function is the heuristic function that estimates the cost from the current
    position to the goal.

    :param state:  Current World state
    :param direction: The action we want to take
    :param goal: Where we want to get
    :return:
    """
    # Obtener una lista de tiles del tile actual al goal_tile empezando con la action cuidando
    # de no regresarnos

    current_tile = state.pacman_tile
    tile_list = find_path(current_tile, current_tile, goal_tile, direction)

    if tile_list == -1:
        return 1.0

    Character.PACMAN.tile_list_options.append((direction, tile_list))

    cost = abs((1.0 / len(tile_list)) - 1.0)
    return cost


def f(state, action, goal_tile):
    return h(state, action, goal_tile)


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
    Character.PACMAN.tile_list_options = []
    mState = WorldState.getState(pointsGroup)
    actions = [GO_UP, GO_LEFT, GO_DOWN, GO_RIGHT]
    pr_list = []
    goal_tile = get_closest_pacman_point(mState)
    Character.PACMAN.goal_tile = goal_tile
    direction = Character.PACMAN.get_closest_direction(mState.current_direction,mState.pacman_tile,goal_tile)

    return direction

def get_closest_direction(dir1, dir2, goal_tile):
    direction = Character.PACMAN.get_direction(Character.PACMAN.facing)
    closest = Character.PACMAN.get_closest_direction(direction, Character.PACMAN.current_tile, goal_tile)
    return closest

def reset_old_direction():
    global OLD_DIRECTION
    OLD_DIRECTION = STAND_STILL
