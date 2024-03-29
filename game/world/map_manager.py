
import pygame
from random import randint, seed
from threading import Thread, Event

from game.data.tiles import Tiles
from game.utils.exceptions import InvalidMapData
from game.utils.logger import logger
from game.world.synth import noise
from game.world.tile_manager import TileManager


class Map:
    """
    Class for creating a Map.
    """


    DEFAULT = ([Tiles.GRASS if randint(0, 8) == 0 else Tiles.PLAINS for x in range(2048)]
               + [Tiles.DIRT if randint(0, 10) == 0 else Tiles.PLAINS for x in range(1024)]
               + [Tiles.DIRT if randint(0, 8) == 0 else Tiles.COBBLESTONE for x in range(2048)])

    SEED_RANGE = 2 ** 32

    def __init__(self, width, height):
        self._data: list = list()
        self._dynatile_data: list = list()
        self._seed = 0
        self._x = -width * TileManager.SIZE // 2
        self._y = -height * TileManager.SIZE // 2
        self._width = width
        self._height = height
        self._surface = None
        self._dynatile_surface = None
        self._ready = False
        self.randomise_seed()
        self.perlin_noise = noise.PerlinNoise()
        self.generate_data_event = Event()
        self.load_data_event = Event()
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def generate(self, game):
        """
        Generate the map data.
        """
        self._ready = False
        self._data.clear()
        self._dynatile_data = [False] * self._width * self._height
        self._surface = pygame.Surface((self._width * TileManager.SIZE, self._height * TileManager.SIZE))
        self._dynatile_surface = pygame.Surface(
            (self._width * TileManager.SIZE, self._height * TileManager.SIZE), pygame.SRCALPHA, 32
        ).convert_alpha()
        game.screens.loading_screen.set_state(True)

        print(f"Generating {self._width * self._height} tiles with seed {self._seed}...")
        game.screens.loading_screen.progress_bar.set_title("Generating map...")
        update_thread = Thread(target=self._generate_data, args=(game,))
        update_thread.start()

        game.screens.loading_screen.update_ui()

        while not self.generate_data_event.is_set():
            game.update_loop()

        game.screens.loading_screen.progress_bar.set_title("Loading map...")
        update_thread = Thread(target=self._load_data, args=(game,))
        update_thread.start()

        game.screens.loading_screen.update_ui()

        while not self.load_data_event.is_set():
            game.update_loop()

        if not self._data:
            raise InvalidMapData

        self.generate_data_event.clear()
        self.load_data_event.clear()
        game.update_all_uis()
        game.player.set_ideal_spawnpoint(game.world.get_map(), game.camera)
        game.screens.loading_screen.set_state(False)
        self._ready = True

    def regenerate(self, game):
        """
        Regenerate the map data.
        """
        self.randomise_seed()
        self.perlin_noise = noise.PerlinNoise()
        self._x = -self.get_width_in_pixels() // 2
        self._y = -self.get_height_in_pixels() // 2
        game.player.reset()
        game.camera.reset()
        self.generate(game)

    def _generate_data(self, game):
        """
        Internal threaded method for generating map data.
        """
        game.screens.loading_screen.progress_bar.set_value(0)
        progress: int = -1
        for tile in range(self._width * self._height):
            noise_value = self.perlin_noise.generate(tile % self._width, tile // self._height)
            if noise_value < -1500:
                self._data.append(Tiles.WATER)
            elif -1500 <= noise_value < -1000:
                self._data.append(Tiles.SAND)
            elif -1000 <= noise_value < -600:
                self._data.append(Tiles.DIRT)
            elif -600 <= noise_value < 0:
                self._data.append(Tiles.GRASS)
            elif 0 <= noise_value < 500:
                self._data.append(Tiles.PLAINS)
            elif 1280 <= noise_value < 1550:
                self._data.append(Tiles.LAVA)
            else:
                self._data.append(Tiles.COBBLESTONE)

            '''if tile > 0:
                if self._data[tile - offset - 1][0] == self._data[tile - offset][0]:
                    self._data.pop()
                    self._data[tile - offset - 1] = (self._data[tile - offset - 1][0], self._data[tile - offset - 1][1] + 1)
                    offset += 1'''

            if progress != round((tile + 1) / (self._width * self._height) * 100):
                progress = round((tile + 1) / (self._width * self._height) * 100)
                game.screens.loading_screen.progress_bar.set_value(progress)
                logger.debug(f'Generating map data... {progress}%')
        self.generate_data_event.set()

    def _load_data(self, game):
        """
        Internal threaded method for loading map data.
        """
        progress: int = -1
        for i, tile in enumerate(self._data):
            x: int = (i % self._width) * TileManager.SIZE
            y: int = TileManager.SIZE * (i // self._width)
            game.world.tile_manager.draw(x, y, tile, self._surface)

            if progress != round((i + 1) / len(self._data) * 100):
                progress = round((i + 1) / len(self._data) * 100)
                game.screens.loading_screen.progress_bar.set_value(progress)
                logger.debug(f'Loading map data... {progress}%')
        self.load_data_event.set()
        '''index = 0
        for i, tile in enumerate(self._data):
            for _ in range(tile[1]):
                x: int = (index % self._width) * TileManager.SIZE
                y: int = TileManager.SIZE * (index // self._width)
                self.game.world.tile_manager.draw(x, y, tile[0], self._surface)
                index += 1
            self.game.screens.loading_screen.progress_bar.set_value(round((i + 1) / len(self._data) * 100))'''    

    def update(self, window_obj, player_obj):
        """
        Update the map (unused).
        """
        pass

    def get_tile_pos(self, x, y):
        """
        Return the tile position of a world position.
        """
        tile_x = round((x - self._x) / TileManager.SIZE)
        tile_y = round((y - self._y) / TileManager.SIZE)
        return tile_x, tile_y

    def get_strict_tile_pos(self, x, y):
        """
        Return the strict tile position of a world position
        """
        tile_x = round(x - self._x) // TileManager.SIZE
        tile_y = round(y - self._y) // TileManager.SIZE
        return tile_x, tile_y

    def tile_to_world_pos(self, tile_x, tile_y):
        """
        Return the world position of a tile position.
        """
        return tile_x * TileManager.SIZE + self._x, tile_y * TileManager.SIZE + self._y

    @staticmethod
    def tile_to_screen_pos(game, tile_x, tile_y):
        """
        Return the screen position of a tile position.
        """
        screen_x, screen_y = game.world.get_map().tile_to_world_pos(tile_x, tile_y)
        return (screen_x - game.camera.x + game.width // 2,
                screen_y - game.camera.y + game.height // 2)

    def is_ready(self):
        """
        Return whether the map is ready or not.
        """
        return self._ready

    def set_tile(self, tile_x, tile_y, tile):
        """
        Set the tile at specified x and y tile positions and of specified tile type, then return the map manager itself.
        """
        self._data[tile_x % self._width + tile_y * self._width] = tile
        return self

    def get_tile(self, tile_x, tile_y):
        """
        Return the tile at specified x and y tile positions.
        """
        return self._data[tile_x % self._width + tile_y * self._width]

    def set_data(self, data: list):
        """
        Set the map data, then return the map manager itself.
        Use default map data if no data is provided.
        """
        if data:
            self._data = data
        else:
            self._data = Map.DEFAULT
        return self

    def get_data(self):
        """
        Return the map data.
        """
        return self._data

    def set_dynatile_data(self, dynatile_data: list):
        """
        Set the dynamic tile data, then return the map manager itself.
        """
        self._dynatile_data = dynatile_data
        return self

    def get_dynatile_data(self):
        """
        Get the dynamic tile data.
        """
        return self._dynatile_data

    def set_dynatile(self, x, y, state):
        """
        Set the dynamic tile at specified x and y tile positions and of specified used state (bool), then return
        the map manager itself.
        """
        self._dynatile_data[y * self._width + x % self._width] = state
        return self

    def get_dynatile(self, x, y):
        """
        Return the dynamic tile at specified x and y tile positions.
        """
        return self._dynatile_data[y * self._width + x % self._width]

    def randomise_seed(self):
        """
        Randomise the map seed, then return the map manager itself.
        """
        self._seed = randint(-Map.SEED_RANGE, Map.SEED_RANGE)
        seed(self._seed)
        return self

    def set_seed(self, _seed):
        """
        Set the map seed, then return the map manager itself.
        """
        self._seed = _seed
        seed(_seed)
        return self

    def get_seed(self):
        """
        Return the map seed.
        """
        return self._seed

    def set_x(self, x):
        """
        Set the x position of the map, then return the map manager itself.
        """
        self._x = x
        return self

    def get_x(self):
        """
        Return the x position of the map.
        """
        return self._x

    def set_y(self, y):
        """
        Set the y position of the map, then return the map manager itself.
        """
        self._y = y
        return self

    def get_y(self):
        """
        Return the y position of the map.
        """
        return self._y

    def get_width_in_tiles(self):
        """
        Return the width of the map in tiles.
        """
        return self._width

    def get_width_in_pixels(self):
        """
        Return the width of the map in pixels.
        """
        return self._width * TileManager.SIZE

    def get_height_in_tiles(self):
        """
        Return the height of the map in tiles.
        """
        return self._height

    def get_height_in_pixels(self):
        """
        Return the height of the map in pixels.
        """
        return self._height * TileManager.SIZE

    def get_surface(self):
        """
        Return the map's surface.
        """
        return self._surface

    def get_dynatile_surface(self):
        """
        Return the map's dynamic surface.
        """
        return self._dynatile_surface
