from numpy import ceil

from game.data.properties.world_properties import WorldProperties
from game.utils.tools import c_log2


class MapStructure:
    """
    Byte structure for the world map.
    """

    MAP_WIDTH_BYTE_SIZE = int(ceil(c_log2(WorldProperties.MAX_MAP_WIDTH) / 8))
    MAP_HEIGHT_BYTE_SIZE = int(ceil(c_log2(WorldProperties.MAX_MAP_HEIGHT) / 8))