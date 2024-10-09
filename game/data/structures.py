
from math import ceil, log2
from typing import SupportsFloat, SupportsIndex

from game.data.properties import TileProperties, WorldProperties


def c_log2(x: SupportsFloat | SupportsIndex, /) -> int:
    return ceil(log2(x))


class MapStructure:
    """
    Byte structure for the world map.
    """

    MAP_WIDTH_BYTE_SIZE = ceil(c_log2(WorldProperties.MAX_MAP_WIDTH) / 8)
    MAP_HEIGHT_BYTE_SIZE = ceil(c_log2(WorldProperties.MAX_MAP_HEIGHT) / 8)


class TileStructure:
    """
    Byte structure for the tile.
    """

    TILE_ID_BYTE_SIZE = c_log2(TileProperties.TILE_ID_MAX)
    TILE_X_BYTE_SIZE = c_log2(TileProperties.TILE_X_MAX)
    TILE_Y_BYTE_SIZE = c_log2(TileProperties.TILE_Y_MAX)
    TILE_RESISTANCE_BYTE_SIZE = c_log2(TileProperties.TILE_RESISTANCE_MAX)
    TILE_DAMAGE_BYTE_SIZE = c_log2(TileProperties.TILE_DAMAGE_MAX)
    TILE_DAMAGE_DELAY_BYTE_SIZE = c_log2(TileProperties.TILE_DAMAGE_DELAY_MAX)

    TILE_BYTE_SIZE = ceil((
        TILE_ID_BYTE_SIZE
        + TILE_X_BYTE_SIZE
        + TILE_Y_BYTE_SIZE
        + TILE_RESISTANCE_BYTE_SIZE
        + TILE_DAMAGE_BYTE_SIZE
        + TILE_DAMAGE_DELAY_BYTE_SIZE
    ) / 8)

    TILE_ID_BYTE_POS = TILE_BYTE_SIZE * 8 - TILE_ID_BYTE_SIZE
    TILE_X_BYTE_POS = TILE_ID_BYTE_POS - TILE_X_BYTE_SIZE
    TILE_Y_BYTE_POS = TILE_X_BYTE_POS - TILE_Y_BYTE_SIZE
    TILE_RESISTANCE_BYTE_POS = TILE_Y_BYTE_POS - TILE_RESISTANCE_BYTE_SIZE
    TILE_DAMAGE_BYTE_POS = TILE_RESISTANCE_BYTE_POS - TILE_DAMAGE_BYTE_SIZE
    TILE_DAMAGE_DELAY_BYTE_POS = TILE_DAMAGE_BYTE_POS - TILE_DAMAGE_DELAY_BYTE_SIZE


class DynatileStructure:
    """
    Byte structure for the dynamic tile.
    No pre-defined dynatile byte size as it can vary.
    """
    
    DYNATILE_STATE_BYTE_SIZE = 1
