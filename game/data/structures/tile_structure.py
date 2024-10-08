from numpy import ceil

from game.data.properties.tile_properties import TileProperties
from game.utils.tools import c_log2


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

    TILE_BYTE_SIZE = int(ceil((
        TILE_ID_BYTE_SIZE
        + TILE_X_BYTE_SIZE
        + TILE_Y_BYTE_SIZE
        + TILE_RESISTANCE_BYTE_SIZE
        + TILE_DAMAGE_BYTE_SIZE
        + TILE_DAMAGE_DELAY_BYTE_SIZE
    ) / 8))

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
