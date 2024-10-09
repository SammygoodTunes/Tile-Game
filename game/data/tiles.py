
from itertools import count
from typing import Self

from game.data.properties import TileProperties
from game.data.structures import TileStructure as TS
from game.utils.logger import logger


class Tile:
    """
    Class for creating a map tile.
    """

    DEFAULT_ATLAS: str = "assets/atlas.png"
    count_id = count()

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self._id: int = next(Tile.count_id)
        self._xy: tuple[int, int] = (x, y)
        self._resistance: int = 0
        self._damage: int = 0
        self._damage_delay: float = 0.0
        assert 0 <= self._xy[0] <= TileProperties.TILE_X_MAX, f'Invalid tile texture coordinates (x): {self._xy[0]}'
        assert 0 <= self._xy[1] <= TileProperties.TILE_Y_MAX, f'Invalid tile texture coordinates (y): {self._xy[1]}'
        assert 0 <= self._resistance <= TileProperties.TILE_RESISTANCE_MAX, f'Invalid tile resistance: {self._resistance}'
        assert 0 <= self._damage <= TileProperties.TILE_DAMAGE_MAX, f'Invalid tile damage: {self._damage}'
        assert 0 <= self._damage_delay <= TileProperties.TILE_DAMAGE_DELAY_MAX, f'Invalid tile damage delay: {self._damage_delay}'
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

    def compress(self) -> int:
        """
        Return the compressed format of the tile's attributes.
        """
        return (
            self._id << TS.TILE_ID_BYTE_POS
            | self._xy[0] << TS.TILE_X_BYTE_POS
            | self._xy[1] << TS.TILE_Y_BYTE_POS
            | self._resistance << TS.TILE_RESISTANCE_BYTE_POS
            | self._damage << TS.TILE_DAMAGE_BYTE_POS
            | int(self._damage_delay * 10) << TS.TILE_DAMAGE_DELAY_BYTE_POS
        )

    def decompress(self, compressed_tile: int) -> Self:
        """
        Extract the tile attributes from the compressed tile and set them accordingly.
        """
        self._id = compressed_tile >> TS.TILE_ID_BYTE_POS
        self._xy = (
            compressed_tile >> TS.TILE_X_BYTE_POS & 2 ** TS.TILE_X_BYTE_SIZE - 1,
            compressed_tile >> TS.TILE_Y_BYTE_POS & 2 ** TS.TILE_Y_BYTE_SIZE - 1
        )
        self._resistance = compressed_tile >> TS.TILE_RESISTANCE_BYTE_POS & 2 ** TS.TILE_RESISTANCE_BYTE_SIZE - 1
        self._damage = compressed_tile >> TS.TILE_DAMAGE_BYTE_POS & 2 ** TS.TILE_DAMAGE_BYTE_SIZE - 1
        self._damage_delay = (compressed_tile >> TS.TILE_DAMAGE_DELAY_BYTE_POS & 2 ** TS.TILE_DAMAGE_DELAY_BYTE_SIZE - 1) / 10
        return self

    def get_id(self):
        """
        Return the id of the tile.
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
