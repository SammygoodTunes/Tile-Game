
from importlib import resources as impr
from itertools import count
from typing import Self

from game.utils.logger import logger


class Tile:
    """
    Class for creating a map tile.
    """

    DEFAULT_ATLAS: str = str(impr.files('assets') / "atlas.png")
    count_id = count()

    def __init__(self, x: int, y: int) -> None:
        self._id: int = next(Tile.count_id)
        self._xy: tuple[int, int] = (x, y)
        self._resistance: int = 0
        self._damage: int = 0
        self._damage_delay: float = 0.0
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def __repr__(self):
        return f'Tile({self._id}, {self._xy}, {self._resistance}, {self._damage}, {self._damage_delay})'

    def __eq__(self, obj: Self):
        if not isinstance(obj, Tile):
            return False
        return (
            self._id == obj.get_id()
            and self._xy == self.get_xy()
            and self._resistance == self.get_resistance()
            and self._damage == self.get_damage()
            and self._damage_delay == self.get_damage_delay()
        )

    def get_id(self):
        """
        Get the id of the tile.
        """
        return self._id

    def set_xy(self, x: int, y: int) -> Self:
        """
        Set the texture coordinates of the tile, then return the tile itself.
        """
        self._xy = (x, y)
        return self

    def get_xy(self) -> tuple[int, int]:
        """
        Return the texture coordinate of the tile.
        """
        return self._xy

    def set_resistance(self, resistance: int) -> Self:
        """
        Set the resistance of the tile, then return the tile itself.
        """
        self._resistance = resistance
        return self

    def get_resistance(self) -> int:
        """
        Return the resistance of the tile.
        """
        return self._resistance

    def set_damage(self, damage: int) -> Self:
        """
        Set the damage amount of the tile, then return the tile itself.
        """
        self._damage = damage
        return self

    def get_damage(self) -> int:
        """
        Return the damage amount of the tile.
        """
        return self._damage

    def set_damage_delay(self, damage_delay: float) -> Self:
        """
        Set the damage delay of the tile, then return the tile itself.
        """
        self._damage_delay = damage_delay
        return self

    def get_damage_delay(self) -> float:
        """
        Return the damage delay of the tile.
        """
        return self._damage_delay


class Tiles:
    """
    Class for creating a collection of tiles.
    """

    VOID: Tile = Tile(0, 0)
    GRASS: Tile = Tile(1, 0)
    PLAINS: Tile = Tile(2, 0)
    DIRT: Tile = Tile(3, 0)
    COBBLESTONE: Tile = Tile(4, 0).set_resistance(10)
    SAND: Tile = Tile(5, 0)
    COBBLESTONE_STAIRS: Tile = Tile(6, 0)
    FIRESTONE: Tile = Tile(7, 0)
    WATER: Tile = Tile(0, 1)
    LAVA: Tile = Tile(1, 1).set_damage(3).set_damage_delay(0.5)
    BREAK_TILES_ANIM: tuple[Tile] = tuple(Tile(x, 7) for x in range(8))


class TileTypes:
    """
    Class for regrouping tiles into different categories.
    """

    PLACEABLE: tuple[Tiles] = (Tiles.GRASS, Tiles.PLAINS, Tiles.DIRT, Tiles.COBBLESTONE, Tiles.SAND,
                               Tiles.COBBLESTONE_STAIRS, Tiles.FIRESTONE, Tiles.WATER, Tiles.LAVA)
    BREAKABLE: tuple[Tiles] = (Tiles.COBBLESTONE,)
    LETHAL: tuple[Tiles] = (Tiles.LAVA,)
