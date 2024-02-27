
from enum import Enum

class Tile:

    DEFAULT_ATLAS: str = "assets/atlas.png"

    def __init__(self, x, y):
        self._xy = (x, y)
        self._resistance: int = 0

    def set_xy(self, x, y):
        self._xy = (x, y)
        return self

    def get_xy(self):
        return self._xy

    def set_resistance(self, resistance: int):
        self._resistance = resistance
        return self

    def get_resistance(self):
        return self._resistance

class Tiles(Enum):
    VOID = Tile(0, 0)
    GRASS = Tile(1, 0)
    PLAINS = Tile(2, 0)
    DIRT = Tile(3, 0)
    COBBLESTONE = Tile(4, 0).set_resistance(10)
    SAND = Tile(5, 0)
    COBBLESTONE_STAIRS = Tile(6, 0)
    FIRESTONE = Tile(7, 0)
    WATER = Tile(0, 1)
    LAVA = Tile(1, 1)

class TileTypes(Enum):
    BREAKABLE = [Tiles.COBBLESTONE]