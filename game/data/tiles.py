
from importlib import resources as impr

from game import assets


class Tile:

    DEFAULT_ATLAS = impr.files(assets) / "atlas.png"

    def __init__(self, x, y):
        self._xy: tuple = (x, y)
        self._resistance: int = 0
        self._damage: int = 0
        self._damage_delay: float = 0.0

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

    def set_damage(self, damage: int):
        self._damage = damage
        return self

    def get_damage(self):
        return self._damage

    def set_damage_delay(self, damage_delay: float):
        self._damage_delay = damage_delay
        return self

    def get_damage_delay(self):
        return self._damage_delay


class Tiles:
    VOID = Tile(0, 0)
    GRASS = Tile(1, 0)
    PLAINS = Tile(2, 0)
    DIRT = Tile(3, 0)
    COBBLESTONE = Tile(4, 0).set_resistance(10)
    SAND = Tile(5, 0)
    COBBLESTONE_STAIRS = Tile(6, 0)
    FIRESTONE = Tile(7, 0)
    WATER = Tile(0, 1)
    LAVA = Tile(1, 1).set_damage(3).set_damage_delay(0.5)
    BREAK_TILES_ANIM = [Tile(x, 7) for x in range(8)]


class TileTypes:
    BREAKABLE = [Tiles.COBBLESTONE]
    LETHAL = [Tiles.LAVA]
