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
from game.data.structures.tile_structure import TileStructure
from game.data.tiles.tile import Tile
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
        self._seed: str = ''
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
        # Somehow make a call to set loading screen state to True

        self.set_state(MapStates.GENMAP)
        logger.info(f"Generating {self._width * self._height} tiles with seed {self._seed}...")
        # Handle info label on loading screen and set it to 'Generating map...'
        progress: int = -1
        timer = time() - GameProperties.LOGGER_DELAY
        for tile_index in range(self._width * self._height):
            noise_value = self.perlin_noise.generate(tile_index % self._width, tile_index // self._height)
            tile: Tile
            if noise_value < -1500:
                tile = Tiles.WATER
            elif -1500 <= noise_value < -1000:
                tile = Tiles.SAND
            elif -1000 <= noise_value < -600:
                tile = Tiles.DIRT
            elif -600 <= noise_value < -300:
                tile = Tiles.PLAINS
            elif -300 <= noise_value < 100:
                tile = Tiles.GRASS
            elif 100 <= noise_value < 500:
                tile = Tiles.PLAINS
            elif 500 <= noise_value < 2000:
                tile = Tiles.COBBLESTONE
            else:
                tile = Tiles.LAVA
            self._tile_data += int.to_bytes(tile.compress(), length=TileStructure.TILE_BYTE_SIZE)

            '''if tile > 0:
                if self._data[tile - offset - 1][0] == self._data[tile - offset][0]:
                    self._data.pop()
                    self._data[tile - offset - 1] = (self._data[tile - offset - 1][0], self._data[tile - offset - 1][1] + 1)
                    offset += 1'''

            current_progress = round((tile_index + 1) / (self._width * self._height) * 100)
            if progress == current_progress:
                continue
            progress = current_progress
            # Set the loading screen progress bar value to 'progress'
            self.set_state(MapStates.GENMAP, progress)
            if time() - timer > GameProperties.LOGGER_DELAY:
                logger.info(f'Generating map data... {progress}%')
                timer = time()
        # Update the loading screen UI to update its info label text

        # Handler info label on loading screen and set it to 'Loading map...'
        '''index = 0
        for i, tile in enumerate(self._data):
            for _ in range(tile[1]):
                x: int = (index % self._width) * TileManager.TILE_SIZE
                y: int = TileManager.TILE_SIZE * (index // self._width)
                self.game.client.world.tile_manager.draw(x, y, tile[0], self._surface)
                index += 1
            self.game.screens.loading_screen.progress_bar.set_value(round((i + 1) / len(self._data) * 100))'''

        # Update the loading screen UI to update its info label text

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

    def regenerate(self, _seed: str) -> None:
        """
        Regenerate the map data.
        """
        if not _seed:
            logger.info('Seed field empty, randomising seed.')
            self.randomise_seed()
        else:
            self.set_seed(_seed)
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
        for i in range(self._width * self._height):
            if not self._dynatile_data:
                break
            x, y = i % self._width, i // self._height
            if self.get_dynatile(x, y) != self.get_dynatile(x, y, ext_bytes_obj=new_dynatile_data):
                self.tile_manager.draw(
                    x * TileProperties.TILE_SIZE,
                    y * TileProperties.TILE_SIZE,
                    Tiles.PLAINS,
                    self._surface
                )
                self.tile_manager.draw(
                    x * TileProperties.TILE_SIZE,
                    y * TileProperties.TILE_SIZE,
                    Tiles.PLAINS,
                    self._dynatile_surface
                )
        self._dynatile_data = new_dynatile_data

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

    def randomise_seed(self) -> Self:
        """
        Randomise the map seed, then return the map manager itself.
        """
        self._seed = ''.join(choice(Map.SEED_CHARS) for _ in range(Map.SEED_LENGTH))
        seed(self._seed)
        return self

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
