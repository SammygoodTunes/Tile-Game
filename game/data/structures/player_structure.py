from numpy import ceil

from game.data.properties.player_properties import PlayerProperties
from game.data.properties.tile_properties import TileProperties
from game.data.properties.world_properties import WorldProperties
from game.utils.tools import c_log2


class PlayerStructure:
    """
    Byte structure for the player.
    """

    PLAYER_NAME_BYTE_SIZE = PlayerProperties.MAX_PLAYER_NAME_SIZE
    PLAYER_X_BYTE_SIZE = int(ceil(c_log2(WorldProperties.MAX_MAP_WIDTH * TileProperties.TILE_SIZE * 2) / 8)) # *2 here because signed
    PLAYER_Y_BYTE_SIZE = int(ceil(c_log2(WorldProperties.MAX_MAP_HEIGHT * TileProperties.TILE_SIZE * 2) / 8))
    PLAYER_BROKEN_TILE_X_BYTE_SIZE = int(ceil(c_log2(WorldProperties.MAX_MAP_WIDTH) / 8))
    PLAYER_BROKEN_TILE_Y_BYTE_SIZE = int(ceil(c_log2(WorldProperties.MAX_MAP_HEIGHT) / 8))
