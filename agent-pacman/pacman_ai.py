__author__ = 'aortegag'

from characters import *
import pygame

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

def get_closest_pacman_point(state):
    h_list = []
    for point in state.dots:
        h = Character.PACMAN.pitagorazo(state.pacman_xy[0]-point.rect.centerx,
                                             state.pacman_xy[1]-point.rect.centery)
        if state.pacman_tile.rect.center != point.rect.center:
            h_list.append((h,point))

    mtuple = min(h_list, key=lambda item:item[0])
    return mtuple[1]

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

def reinforcement_learning_get_direction(pointsGroup):
    """
    This function is the one that learns the game and determines which direction
    should pac man go.

    This algorithm can see and knows about the same things as a human player, i.e.
    the position of each ghost, the position of each point.

    Pac man will have to learn what happens when it eats an energizer point, also
    he has to learn when to reverse direction.
    :return:
    """
    mState = WorldState.getState(pointsGroup)
    actions = getPossibleActions()
    pr_list = []
    for action in actions:
        pr = agent_policy(mState, action, len(actions))
        if pr != 0:
            pr_list.append((pr, action))

    max_tuple = max(pr_list, key=lambda item:item[0])
    return max_tuple[1]
