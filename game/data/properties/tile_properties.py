"""
Module name: tile_properties

This module defines the tile properties.
"""

from game.data.properties.world_properties import WorldProperties



class TileProperties:
    """
    Class for tile properties.
    """

    TILE_SIZE = 32
    TILE_X_MAX = 7
    TILE_Y_MAX = 7
    TILE_RESISTANCE_MAX = 63
    TILE_DAMAGE_MAX = 127
    TILE_DAMAGE_DELAY_MAX = 0.8 * 10
    TILE_ADJACENT_DUPLICATES_MAX = WorldProperties.MAX_MAP_WIDTH * WorldProperties.MAX_MAP_HEIGHT
