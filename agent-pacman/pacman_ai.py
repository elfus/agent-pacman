__author__ = 'aortegag'

from characters import *
import pygame

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


def get_closest_pacman_point(state):
    """
    Gets the closest pacman point to pacman in terms of number of tiles in a path.

    @BUG This function has a problem when two different paths have the same length, the one
    that will be chosen is the first occurrence in the list. We have to randomize that somehow

    :param state:
    :return:
    """
    current_tile = state.pacman_tile
    list_of_list = find_pacman_points(current_tile, current_tile)

    # TODO: Randomize the choosing of two lists with the same path cost
    list = min(list_of_list, key=lambda list: len(list))

    last_point = list[-1]

    return last_point


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

    if current_tile == goal_tile:
        tile_list.append(current_tile)
        return tile_list

    if is_going_away_from_goal(current_tile,goal_tile,direction) == True:
        return -1

    facing_to = Character.PACMAN.get_facing(direction)
    adjacent_tile, tile_xy = Character.PACMAN.get_adjacent_tile_to(current_tile, facing_to)
    if adjacent_tile.is_walkable == False:
        adjacent_tile = current_tile
    tile_list.append(current_tile)
    direction = Character.PACMAN.get_closest_direction_excluding(direction, adjacent_tile, goal_tile, tile_list)
    subpath = find_path(adjacent_tile, current_tile, goal_tile, direction)
    tile_list.extend(subpath)
    return tile_list


def get_real_tile(state):
    real_tile = 0
    x = state.pacman_tile.board_coordinate[0]
    y = state.pacman_tile.board_coordinate[1]

    #This means we are on the same row
    if state.pacman_xy[0] == state.pacman_tile.rect.centerx:
        # it means pacman is below the current tile center
        if state.pacman_xy[1] > state.pacman_tile.rect.centery:
            x = state.pacman_tile.board_coordinate[0]
            y = state.pacman_tile.board_coordinate[1] + 1
        # it means pacman is above the current tile center
        if state.pacman_xy[1] < state.pacman_tile.rect.centery:
            x = state.pacman_tile.board_coordinate[0]
            y = state.pacman_tile.board_coordinate[1] - 1
    # This means we are on the same column
    elif state.pacman_xy[1] == state.pacman_tile.rect.centery:
        # it means pacman is to the right of the current tile center
        if state.pacman_xy[0] > state.pacman_tile.rect.centerx:
            x = state.pacman_tile.board_coordinate[0] + 1
            y = state.pacman_tile.board_coordinate[1]
        # it means pacman is to the left of the current tile center
        if state.pacman_xy[0] < state.pacman_tile.rect.centerx:
            x = state.pacman_tile.board_coordinate[0] - 1
            y = state.pacman_tile.board_coordinate[1]

    real_tile = Character.PACMAN.board_matrix[x][y]
    return real_tile


def prune_list(tile_list, goal_tile):
    """
    This function iterates over the tiles in the list, and if any of those tiles happens
    to be a neighbor from the goal_tile then it's pruned.
    """
    i = 0
    new_list = []
    while i < len(tile_list):
        tile = tile_list[i]
        neighbors = get_tile_neighbors(Character.PACMAN.board_matrix, tile)
        if goal_tile in neighbors:
            new_list = tile_list[:i + 1]
            new_list.extend(tile_list[-1:])
            break
        i += 1

    return new_list


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

    if len(tile_list) == 0:
        return 0.0

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
    mState = WorldState.getState(pointsGroup)
    actions = [GO_UP, GO_LEFT, GO_DOWN, GO_RIGHT]
    pr_list = []
    goal_tile = get_closest_pacman_point(mState)
    # ppoint_tile = get_tile_from_pacman_point(ppoint)
    for action in actions:
        pr_list.append((f(mState, action, goal_tile), action))

    #This is meant to cover the case in which  we get two options with the
    # same probability, we choose to continue with the same direction we had
    if goal_tile == mState.pacman_tile:
        for opt in pr_list:
            if opt[1] == action:
                return OLD_DIRECTION


    # The value f() returns represents the risk to take that action
    # The lower the risk the better option it looks
    min_tuple = min(pr_list, key=lambda item: item[0])
    OLD_DIRECTION = min_tuple[1]

    i = 0
    j = 0
    while i < len(pr_list):
        opt1 = pr_list[i]
        j = i + 1
        while j < len(pr_list):
            opt2 = pr_list[j]
            if opt1[0] == opt2[0]:
                if opt1[0] <= min_tuple[0]:
                    return OLD_DIRECTION
            j += 1
        i += 1

    return min_tuple[1]


def reset_old_direction():
    global OLD_DIRECTION
    OLD_DIRECTION = STAND_STILL
