"""
Module name: keys

This module defines all the hotkeys, linked to specific in-game actions.
"""

from pygame import (
    K_SPACE,
    K_TAB,
    K_d,
    K_q,
    K_s,
    K_z,
)


class Keys:
    """
    Class for regrouping all the keys associated to different game actions.
    """

    MOVE_DOWN = K_s
    MOVE_LEFT = K_q
    MOVE_RIGHT = K_d
    MOVE_UP = K_z
    SHOW_MAP = K_SPACE
    SHOW_PLAYERLIST = K_TAB
