"""
Module name: map_manager

This module manages the generation, data and updates of the world map.
"""

from math import ceil
from pygame import SRCALPHA, Surface
from random import choice, seed
from string import ascii_letters, digits
from time import time
from typing import Self

from game.data.properties.game_properties import GameProperties
from game.data.properties.tile_properties import TileProperties
from game.data.properties.world_properties import WorldProperties
from game.data.states.map_states import MapStates
from game.data.structures.tile_structure import TileStructure, DynatileStructure
from game.data.themes.theme_layers import ThemeLayers
from game.data.tiles.tile import Tile
from game.data.tiles.tile_types import TileTypes
from game.data.tiles.tiles import Tiles
from game.utils.exceptions import InvalidMapData
from game.utils.logger import logger
from game.world.synth import noise
from game.world.tile_manager import TileManager


class Map:
    """
    Class for creating a Map.
    """

    SEED_LENGTH: int = 64
    SEED_CHARS: str = ''.join(digits + ascii_letters)

    def __init__(self, width: int, height: int) -> None:
        assert WorldProperties.MIN_MAP_WIDTH <= width <= WorldProperties.MAX_MAP_WIDTH, 'Unauthorised map dimensions'
        assert WorldProperties.MIN_MAP_HEIGHT <= height <= WorldProperties.MAX_MAP_HEIGHT, 'Unauthorised map dimensions'
        self._state: tuple[str, int] = ('', 0)
        self.tile_manager = TileManager()
        self._dynatile_data: bytes = b''
        self._tile_data: bytes = b''
        self._compressed_tile_data: bytes = b''
        self._compressed_dynatile_data: bytes = b''
        self._seed: str = ''
        self._theme: dict = {}
        self._x = -width * TileProperties.TILE_SIZE // 2
        self._y = -height * TileProperties.TILE_SIZE // 2
        self._width = width
        self._height = height
        self._surface = Surface((0, 0))
        self._dynatile_surface = Surface((0, 0))
        self.perlin_noise = noise.PerlinNoise()

    def initialise(self) -> None:
        """
        Initialise the map manager.
        """
        self._x = -self._width * TileProperties.TILE_SIZE // 2
        self._y = -self._height * TileProperties.TILE_SIZE // 2
        self._surface = Surface((self._width * TileProperties.TILE_SIZE, self._height * TileProperties.TILE_SIZE))
        self._dynatile_surface = Surface(
            (self._width * TileProperties.TILE_SIZE, self._height * TileProperties.TILE_SIZE), SRCALPHA, 32
        ).convert_alpha()

    def generate(self) -> None:
        """
        Generate the map data.
        """
        self._tile_data = b''
        self._dynatile_data = b'\x00' * ceil(self._width * self._height / 8)
        progress: int = -1
        # Somehow make a call to set loading screen state to True

        self.set_state(MapStates.GENMAP)
        logger.info(f"Generating {self._width * self._height} tiles with seed {self._seed}...")
        # Handle info label on loading screen and set it to 'Generating map...'

        timer = time() - GameProperties.LOGGER_DELAY
        self.perlin_noise.MIN_HEIGHT = 0
        self.perlin_noise.MAX_HEIGHT = 0
        for tile_index in range(self._width * self._height):
            noise_value = self.perlin_noise.generate(tile_index % self._width, tile_index // self._height)
            tile: Tile

            for layer in self._theme['layers']:
                if layer['type'] == ThemeLayers.LAYER_B:
                    if not noise_value < layer['max_height']:
                        continue
                elif layer['type'] == ThemeLayers.LAYER_T:
                    if not noise_value >= layer['min_height']:
                        continue
                elif layer['type'] == ThemeLayers.LAYER_C:
                    if not layer['min_height'] <= noise_value < layer['max_height']:
                        continue
                tile = vars(Tiles)[layer['tile']]
                if (
                        tile_index == self._width // 2 + self._height * (self._height // 2 - 1) or
                        tile_index == self._width // 2 + self._height * self._height // 2 or
                        tile_index == self._width // 2 - 1 + self._height * (self._height // 2 - 1) or
                        tile_index == self._width // 2 - 1 + self._height * self._height // 2
                ) and (tile in TileTypes.BREAKABLE or tile in TileTypes.LETHAL):
                    tile = Tiles.DIRT
                self._tile_data += int.to_bytes(tile.compress(), length=TileStructure.TILE_BYTE_SIZE)
                break

            current_progress = round((tile_index + 1) / (self._width * self._height) * 100)
            if progress == current_progress:
                continue
            progress = current_progress

            self.set_state(MapStates.GENMAP, progress)
            if time() - timer > GameProperties.LOGGER_DELAY:
                logger.info(f'Generating map data... {progress}%')
                timer = time()

        logger.info('Compressing map...')
        self.compress_tile_data()
        self.compress_dynatile_data()

        logger.debug(f'Generated map with {self.perlin_noise.MIN_HEIGHT=} {self.perlin_noise.MAX_HEIGHT=}')

        if not self._tile_data:
            raise InvalidMapData


    def load(self) -> None:
        """
        Decompress and draw the map tiles to the surface.
        """
        progress: int = -1
        timer = time() - GameProperties.LOGGER_DELAY
        for i in range(len(self._tile_data) // TileStructure.TILE_BYTE_SIZE):
            x: int = (i % self._width) * TileProperties.TILE_SIZE
            y: int = TileProperties.TILE_SIZE * (i // self._width)
            tile = Tile().decompress(
                int.from_bytes(
                    self._tile_data[i * TileStructure.TILE_BYTE_SIZE:i * TileStructure.TILE_BYTE_SIZE + TileStructure.TILE_BYTE_SIZE]
                )
            )
            self.tile_manager.draw(x, y, tile, self._surface)
            current_progress = round((i + 1) / (len(self._tile_data) // TileStructure.TILE_BYTE_SIZE) * 100)
            if progress == current_progress:
                continue
            progress = current_progress
            if time() - timer > GameProperties.LOGGER_DELAY:
                logger.info(f'Loading map data... {progress}%')
                timer = time()
        logger.info('Done!')
        self.set_state(MapStates.READY)

    def regenerate(self, _seed: str, theme: dict) -> None:
        """
        Regenerate the map data.
        """
        if not _seed:
            logger.info('Seed field empty, randomising seed.')
            self.randomise_seed()
        else:
            self.set_seed(_seed)
        self._theme = theme
        self.perlin_noise = noise.PerlinNoise()
        self._x = -self.get_width_in_pixels() // 2
        self._y = -self.get_height_in_pixels() // 2
        # Call player and camera reset() here
        self.generate()

    def update(self, new_dynatile_data: bytes) -> None:
        """
        Update the old dynatile data with new dynatile data.
        Only update the differences between the two.
        """
        if self._compressed_dynatile_data == new_dynatile_data:
            return
        self.decompress_dynatile_data()
        dynatile_data = self.decompress_dynatile_data(ext_bytes_obj=new_dynatile_data)

        for i in range(self._width * self._height):
            if not self._dynatile_data:
                break
            x, y = i % self._width, i // self._height
            if self.get_dynatile(x, y) != self.get_dynatile(x, y, ext_bytes_obj=dynatile_data):
                self.set_tile(x, y, Tiles.DIRT)
                self.tile_manager.draw(
                    x * TileProperties.TILE_SIZE,
                    y * TileProperties.TILE_SIZE,
                    Tiles.DIRT,
                    self._surface
                )
                self.tile_manager.draw(
                    x * TileProperties.TILE_SIZE,
                    y * TileProperties.TILE_SIZE,
                    Tiles.DIRT,
                    self._dynatile_surface
                )

        self._compressed_dynatile_data = new_dynatile_data
        self._dynatile_data = dynatile_data

    def compress_tile_data(self) -> Self:
        """
        Compress the map's tile data, then return the map manager itself.
        """
        previous_tile: int = -1
        amount: int = 1
        self._compressed_tile_data: bytes = b''
        length: int = len(self._tile_data) // TileStructure.TILE_BYTE_SIZE
        for i in range(length):
            tile = int.from_bytes(
                    self._tile_data[
                        i * TileStructure.TILE_BYTE_SIZE
                        :i * TileStructure.TILE_BYTE_SIZE + TileStructure.TILE_BYTE_SIZE
                    ]
            )

            if previous_tile < 0:
                previous_tile = tile
                continue

            if previous_tile == tile:
                amount += 1
            else:
                self._compressed_tile_data += (
                        int.to_bytes(previous_tile, length=TileStructure.TILE_BYTE_SIZE)
                        + int.to_bytes(amount, length=TileStructure.TILE_ADJACENT_DUPLICATES_BYTE_SIZE)
                )
                amount = 1
                previous_tile = tile

            if i == length - 1:
                self._compressed_tile_data += (
                        int.to_bytes(tile, length=TileStructure.TILE_BYTE_SIZE)
                        + int.to_bytes(amount, length=TileStructure.TILE_ADJACENT_DUPLICATES_BYTE_SIZE)
                )
        return self

    def decompress_tile_data(self) -> Self:
        """
        Decompress the map's tile data, then return the map manager itself.
        """
        self._tile_data = b''
        sector_size = (TileStructure.TILE_BYTE_SIZE + TileStructure.TILE_ADJACENT_DUPLICATES_BYTE_SIZE)
        for i in range(len(self._compressed_tile_data) // sector_size):
            tile = int.from_bytes(
                self._compressed_tile_data[
                    i * sector_size
                    :i * sector_size + TileStructure.TILE_BYTE_SIZE
                ]
            )
            amount = int.from_bytes(
                self._compressed_tile_data[
                    i * sector_size + TileStructure.TILE_BYTE_SIZE
                    :i * sector_size + sector_size
                ]
            )
            self._tile_data += int.to_bytes(tile, length=TileStructure.TILE_BYTE_SIZE) * amount
        return self

    def compress_dynatile_data(self) -> Self:
        """
        Compress the map's dynatile data, then return the map manager itself.
        """
        previous_dynatile: int = -1
        amount: int = 1
        self._compressed_dynatile_data: bytes = b''
        length: int = len(self._dynatile_data)
        for i in range(length):
            if previous_dynatile < 0:
                previous_dynatile = self._dynatile_data[i]
                continue

            if previous_dynatile == self._dynatile_data[i]:
                amount += 1
            else:
                self._compressed_dynatile_data += (
                        int.to_bytes(previous_dynatile, length=DynatileStructure.DYNATILE_STATE_BYTE_SIZE)
                        + int.to_bytes(amount, length=DynatileStructure.DYNATILE_ADJACENT_DUPLICATES_BYTE_SIZE)
                )
                amount = 1
                previous_dynatile = self._dynatile_data[i]

            if i == length - 1:
                self._compressed_dynatile_data += (
                        int.to_bytes(self._dynatile_data[i], length=DynatileStructure.DYNATILE_STATE_BYTE_SIZE)
                        + int.to_bytes(amount, length=DynatileStructure.DYNATILE_ADJACENT_DUPLICATES_BYTE_SIZE)
                )
        return self

    def decompress_dynatile_data(self, ext_bytes_obj: bytes | None = None) -> bytes | Self:
        """
        Decompress the map's dynatile data.
        Return the decompressed dynatile data if external bytes object is provided, otherwise the map manager itself.
        """
        dynatile_data = b''
        compressed_dynatile_data = self._compressed_dynatile_data if ext_bytes_obj is None else ext_bytes_obj
        sector_size = (DynatileStructure.DYNATILE_STATE_BYTE_SIZE + DynatileStructure.DYNATILE_ADJACENT_DUPLICATES_BYTE_SIZE)
        for i in range(len(compressed_dynatile_data) // sector_size):
            dynatile = int.from_bytes(
                compressed_dynatile_data[
                    i * sector_size
                    :i * sector_size + DynatileStructure.DYNATILE_STATE_BYTE_SIZE
                ]
            )
            amount = int.from_bytes(
                compressed_dynatile_data[
                    i * sector_size + DynatileStructure.DYNATILE_STATE_BYTE_SIZE
                    :i * sector_size + sector_size
                ]
            )
            dynatile_data += int.to_bytes(dynatile, length=DynatileStructure.DYNATILE_STATE_BYTE_SIZE) * amount
        if ext_bytes_obj is not None:
            return dynatile_data
        self._dynatile_data = dynatile_data
        return self

    def set_state(self, state: str = '', value: int = 0) -> Self:
        """
        Set the state of the map manager, then return the map manager itself.
        """
        self._state = (state, value)
        return self

    def get_state(self) -> tuple[str, int]:
        """
        Return the state of the map manager.
        """
        return self._state

    def get_tile_pos(self, x: int, y: int) -> tuple[int, int]:
        """
        Return the tile position of a world position.
        """
        tile_x = round((x - self._x) / TileProperties.TILE_SIZE)
        tile_y = round((y - self._y) / TileProperties.TILE_SIZE)
        return tile_x, tile_y

    def get_strict_tile_pos(self, x: int, y: int) -> tuple[int, int]:
        """
        Return the strict tile position of a world position
        """
        tile_x = round(x - self._x) // TileProperties.TILE_SIZE
        tile_y = round(y - self._y) // TileProperties.TILE_SIZE
        return tile_x, tile_y

    def tile_to_world_pos(self, tile_x: int, tile_y: int) -> tuple[int, int]:
        """
        Return the world position of a tile position.
        """
        return tile_x * TileProperties.TILE_SIZE + self._x, tile_y * TileProperties.TILE_SIZE + self._y

    def tile_to_screen_pos(self, game, tile_x: int, tile_y: int) -> tuple[int, int]:
        """
        Return the screen position of a tile position.
        """
        world_x, world_y = self.tile_to_world_pos(tile_x, tile_y)
        return int(game.width // 2 + world_x - int(game.client.camera.x)), int(game.height // 2 + world_y - int(game.client.camera.y))

    def draw_tile(self, tile_x: int, tile_y: int, tile: Tile | int) -> Self:
        """
        Draw a specific tile to the screen at specified x and y tile positions, then return the map manager itself.
        """
        self.tile_manager.draw(tile_x, tile_y, tile, self._surface)
        return self

    def set_tile(self, tile_x: int, tile_y: int, tile: Tile | int) -> Self:
        """
        Set the tile at specified x and y tile positions and of specified tile type, then return the map manager itself.
        """
        if isinstance(tile, Tile):
            tile = tile.compress()
        pos = TileStructure.TILE_BYTE_SIZE * (tile_x % self._width + tile_y * self._width)
        self._tile_data = (
                self._tile_data[:pos]
                + int.to_bytes(tile, length=TileStructure.TILE_BYTE_SIZE)
                + self._tile_data[pos + TileStructure.TILE_BYTE_SIZE:]
        )
        return self

    def get_tile(self, tile_x: int, tile_y: int) -> Tile:
        """
        Return the tile at specified x and y tile positions.
        """
        pos = TileStructure.TILE_BYTE_SIZE * (tile_x % self._width + tile_y * self._width)
        return Tile().decompress(int.from_bytes(self._tile_data[pos:pos + TileStructure.TILE_BYTE_SIZE]))

    def set_tile_data(self, tile_data: bytes) -> Self:
        """
        Set the map's tile data, then return the map manager itself.
        """
        self._tile_data = tile_data
        return self

    def get_tile_data(self) -> bytes:
        """
        Return the map's tile data.
        """
        return self._tile_data

    def set_compressed_tile_data(self, compressed_tile_data: bytes) -> Self:
        """
        Set the map's compressed tile data, then return the map manager itself.
        The provided compressed tile data must be of same origin as that generated from the map manager's
        tile data compression method.
        """
        self._compressed_tile_data = compressed_tile_data
        return self

    def get_compressed_tile_data(self) -> bytes:
        """
        Return the map's compressed tile data.
        """
        return self._compressed_tile_data

    def set_dynatile_data(self, dynatile_data: bytes):
        """
        Set the map's dynamic tile data, then return the map manager itself.
        """
        self._dynatile_data = dynatile_data
        return self

    def get_dynatile_data(self) -> bytes:
        """
        Get the map's dynamic tile data.
        """
        return self._dynatile_data

    def set_dynatile(self, tile_x: int, tile_y: int, tile_state: bool) -> Self:
        """
        Set the dynamic tile at specified x and y tile positions and of specified used state (bool), then return
        the map manager itself.
        """
        byte_pos = (tile_x % self._width + tile_y * self._width) // 8
        new_tile_byte = (
            self._dynatile_data[byte_pos]
            | (1 << 0x7 - (tile_x % self._width + tile_y * self._width) % 8)) if tile_state else (
            self._dynatile_data[byte_pos] & ~(1 << 0x7 - (tile_x % self._width + tile_y * self._width) % 8)
        )
        self._dynatile_data = (
                self._dynatile_data[:byte_pos]
                + int.to_bytes(new_tile_byte)
                + self._dynatile_data[byte_pos + 1:]
        )
        return self

    def get_dynatile(self, tile_x: int, tile_y: int, ext_bytes_obj: bytes = b'') -> bool:
        """
        Return the dynamic tile state at specified x and y tile positions.
        Extract from an external compatible bytes object if one is given.
        """
        array_index = tile_x % self._width + tile_y * self._width
        byte_pos = array_index // 8
        if not ext_bytes_obj:
            return bool(self._dynatile_data[byte_pos] >> (0x7 - array_index % 8) & 1)
        return bool(ext_bytes_obj[byte_pos] >> (0x7 - array_index % 8) & 1)

    def set_compressed_dynatile_data(self, compressed_dynatile_data: bytes) -> Self:
        """
        Set the map's compressed dynatile data, then return the map manager itself.
        The provided compressed dynatile data must be of same origin as that generated from the map manager's
        dynatile data compression method.
        """
        self._compressed_dynatile_data = compressed_dynatile_data
        return self

    def get_compressed_dynatile_data(self) -> bytes:
        """
        Return the map's compressed dynatile data.
        """
        return self._compressed_dynatile_data

    def randomise_seed(self) -> Self:
        """
        Randomise the map seed, then return the map manager itself.
        """
        self._seed = ''.join(choice(Map.SEED_CHARS) for _ in range(Map.SEED_LENGTH))
        seed(self._seed)
        return self

    @staticmethod
    def get_size_from_property(_property: str) -> tuple[int, int]:
        """
        Return the appropriate map size (width, height) from the provided map property string value.
        """
        if _property == WorldProperties.MAP_SMALL:
            return 64, 64
        if _property == WorldProperties.MAP_MEDIUM:
            return 128, 128
        if _property == WorldProperties.MAP_LARGE:
            return 192, 192
        logger.warn(f'Unknown map size {_property}, defaulting to {WorldProperties.MAP_SMALL})')
        return 64, 64

    def set_seed(self, _seed: str) -> Self:
        """
        Set the map seed, then return the map manager itself.
        """
        self._seed = _seed
        seed(_seed)
        return self

    def get_seed(self) -> str:
        """
        Return the map seed.
        """
        return self._seed

    def set_x(self, x: int) -> Self:
        """
        Set the x position of the map, then return the map manager itself.
        """
        self._x = x
        return self

    def get_x(self) -> int:
        """
        Return the x position of the map.
        """
        return self._x

    def set_y(self, y: int) -> Self:
        """
        Set the y position of the map, then return the map manager itself.
        """
        self._y = y
        return self

    def get_y(self) -> int:
        """
        Return the y position of the map.
        """
        return self._y

    def set_size_in_tiles(self, width: int, height: int) -> Self:
        """
        Set the width and height of the map in tiles, then return the map manager itself.
        """
        self._width, self._height = width, height
        return self

    def get_width_in_tiles(self) -> int:
        """
        Return the width of the map in tiles.
        """
        return self._width

    def get_width_in_pixels(self) -> int:
        """
        Return the width of the map in pixels.
        """
        return self._width * TileProperties.TILE_SIZE

    def get_height_in_tiles(self) -> int:
        """
        Return the height of the map in tiles.
        """
        return self._height

    def get_height_in_pixels(self) -> int:
        """
        Return the height of the map in pixels.
        """
        return self._height * TileProperties.TILE_SIZE

    def get_surface(self) -> Surface:
        """
        Return the map's surface.
        """
        return self._surface

    def get_dynatile_surface(self) -> Surface:
        """
        Return the map's dynamic surface.
        """
        return self._dynatile_surface
