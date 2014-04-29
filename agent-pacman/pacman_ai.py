__author__ = 'aortegag'

from characters import *

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

def agent_policy(state, action):
    """
    Calculates the probability that the action will be performed in the current state
    :param state:
    :param action:
    :return:
    """

    return 1

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
        pr = agent_policy(mState, action)
        pr_list.append((pr, action))

    max_tuple = max(pr_list)
    return max_tuple[1]
