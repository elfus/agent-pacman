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
            self.ghost_list.append((ghost.rect.center,ghost.current_tile))
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
        if current_tile.board_coordinate == (0,17):
            sublist = []
            sublist.append(current_tile)
            new_tile = Character.PACMAN.board_matrix[TILE_WIDTH_COUNT-1][17]
            tile_eaten = find_pacman_points(new_tile, current_tile)
            sublist.extend(tile_eaten[-1])
            tile_list.append(sublist)
        elif current_tile.board_coordinate == (TILE_WIDTH_COUNT-1,17):
            sublist = []
            sublist.append(current_tile)
            new_tile = Character.PACMAN.board_matrix[0][17]
            tile_eaten = find_pacman_points(new_tile, current_tile)
            sublist.extend(tile_eaten[-1])
            tile_list.append(sublist)

    current_tile.visited = False
    return tile_list


def get_closest_pacman_point(state):
    list_of_list = []
    h_list = []

    current_tile = state.pacman_tile
    list_of_list = find_pacman_points(current_tile, current_tile)

    list = min(list_of_list, key=lambda list: len(list))

    last_point = list[-1]

    return last_point

def get_tile_from_pacman_point(ppoint):
    board = Character.PACMAN.board_matrix
    i  = 0
    for row in board:
        for tile in row:
            if ppoint.rect.center == tile.rect.center:
                return tile
    return 0

def reward_function(state, action, number_actions):
    """
    The reward function tells pacman what is good in an immediate sense. It tells pacman
    the desirability to apply the given action in the current state

    """
    ppoint = get_closest_pacman_point(state)
    ppoint_tile = get_tile_from_pacman_point(ppoint)
    desired_direction = Character.PACMAN.get_direction_from_to(state.pacman_tile,ppoint_tile)
    pr = 1.0/number_actions

    return pr


def agent_policy(state, action, number_actions):
    """
    Calculates the probability that the action will be performed in the current state
    :param state:
    :param action:
    :return:
    """
    val = reward_function(state, action, number_actions)
    return val


def g(state, action):
    """
    The g() function returns the cost from the initial node to the actual position

    :param state: Current World state
    :param action: The action we want to take
    :return:
    """
    return 0

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
    tile_list = []
    current_tile = state.pacman_tile

    # TODO: Cambiar este algoritmo, NECESITAS USAR LA LISTA DE TILES QUE YA SE GENERA
    # EN LA FUNCION RECURSIVA!! ESE ES EL CAMINO A SEGUIR :)
    while current_tile != goal_tile:
        facing_to = Character.PACMAN.get_facing(direction)
        adjacent_tile, tile_xy = Character.PACMAN.get_adjacent_tile_to(current_tile, facing_to)
        if adjacent_tile not in tile_list:
            tile_list.append(adjacent_tile)
            current_tile = adjacent_tile
            direction = Character.PACMAN.get_closest_direction_excluding(direction, current_tile, goal_tile,tile_list)

    if len(tile_list) == 0:
        return 0.0

    cost = abs( (1.0/len(tile_list)) - 1.0 )
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
    actions = getPossibleActions()
    pr_list = []
    ppoint_tile = get_closest_pacman_point(mState)
    # ppoint_tile = get_tile_from_pacman_point(ppoint)
    for action in actions:
        pr_list.append( (f(mState, action, ppoint_tile), action) )



    #This is meant to cover the case in which  we get two options with the
    # same probability, we choose to continue with the same direction we had
    if ppoint_tile == mState.pacman_tile:
        for opt in pr_list:
            if opt[1] == action:
                return OLD_DIRECTION


    # The value f() returns represents the risk to take that action
    # The lower the risk the better option it looks
    min_tuple = min(pr_list, key=lambda item:item[0])
    OLD_DIRECTION = min_tuple[1]

    i = 0
    j = 0
    while i < len(pr_list):
        opt1 = pr_list[i]
        j = i + 1
        while j < len(pr_list):
            opt2 = pr_list[j]
            if opt1[0] == opt2[0]:
                return OLD_DIRECTION
            j += 1
        i += 1

    return min_tuple[1]
