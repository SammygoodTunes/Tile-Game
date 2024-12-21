"""
Module name: map_structure

This module defines the byte (or data packet) structure for the world map.
"""

from math import ceil

from game.data.properties.tile_properties import TileProperties
from game.data.properties.world_properties import WorldProperties
from game.data.structures.tile_structure import TileStructure, DynatileStructure
from game.utils.tools import c_log2


class MapStructure:
    """
    Byte structure for the map.
    """

    MAP_WIDTH_BYTE_SIZE = int(ceil(c_log2(WorldProperties.MAX_MAP_WIDTH) / 8))
    MAP_HEIGHT_BYTE_SIZE = int(ceil(c_log2(WorldProperties.MAX_MAP_HEIGHT) / 8))
    MAP_TD_LEN_BYTE_SIZE = int(ceil(c_log2(
        (TileStructure.TILE_BYTE_SIZE + TileStructure.TILE_ADJACENT_DUPLICATES_BYTE_SIZE)
        * TileProperties.TILE_ADJACENT_DUPLICATES_MAX
    ) / 8))
    MAP_DTD_LEN_BYTE_SIZE = int(ceil(c_log2(
        (DynatileStructure.DYNATILE_STATE_BYTE_SIZE + DynatileStructure.DYNATILE_ADJACENT_DUPLICATES_BYTE_SIZE)
        * (TileProperties.TILE_ADJACENT_DUPLICATES_MAX / 8)
    ) / 8))
