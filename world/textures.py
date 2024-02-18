
from enum import Enum


class Textures(Enum):
    VOID = 0x0
    GRASS = 0x1
    PLAINS = 0x2
    DIRT = 0x3
    COBBLESTONE = 0x4
    SAND = 0x5
    COBBLESTONE_STAIRS = 0x6
    FIRESTONE = 0x7
    WATER = 0x8
    LAVA = 0x9

class Tiles(Enum):
    BREAKABLE = [Textures.COBBLESTONE]