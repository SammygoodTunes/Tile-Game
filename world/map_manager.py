from .texture_manager import Textures, Tiles, Texture
from utils.exceptions import InvalidMapData
from .synth import noise

import pygame
from pygame.math import clamp
from random import randint, seed, random
from threading import Thread, Event


class Map:
    DEFAULT = ([Textures.GRASS if randint(0, 8) == 0 else Textures.PLAINS for x in range(2048)]
               + [Textures.DIRT if randint(0, 10) == 0 else Textures.PLAINS for x in range(1024)]
               + [Textures.DIRT if randint(0, 8) == 0 else Textures.COBBLESTONE for x in range(2048)])

    SEED_RANGE = 2**32

    def __init__(self, game, width, height):
        self.game = game
        self._data: list = list()
        self._dynatile_data: list = list()
        self._seed = 0
        self._x = -width * Texture.SIZE // 2
        self._y = -height * Texture.SIZE // 2
        self._width = width
        self._height = height
        self._surface = None
        self._dynatile_surface = None
        self.randomise_seed()
        self.perlin_noise = noise.PerlinNoise()
        self.generate_data_event = Event()
        self.load_data_event = Event()

    def generate(self, texture_obj):
        self._data.clear()
        self._dynatile_data = [False] * self._width * self._height
        self._surface = pygame.Surface((self._width * Texture.SIZE, self._height * Texture.SIZE))
        self._dynatile_surface = pygame.Surface((self._width * Texture.SIZE, self._height * Texture.SIZE), pygame.SRCALPHA, 32).convert_alpha()
        self.game.screens.loading_screen.set_state(True)
        offset = 0

        print(f"Generating {self._width * self._height} tiles with seed {self._seed}...")
        self.game.screens.loading_screen.progress_bar.set_title("Generating map...")
        update_thread = Thread(target=self.generate_data)
        update_thread.start()

        self.game.screens.loading_screen.update_ui()

        while not self.generate_data_event.is_set():
            self.game.update_loop()

        self.game.screens.loading_screen.progress_bar.set_title("Loading map...")
        update_thread = Thread(target=self.load_data, args=(texture_obj,))
        update_thread.start()

        self.game.screens.loading_screen.update_ui()

        while not self.load_data_event.is_set():
            self.game.update_loop()

        if not self._data:
            raise InvalidMapData

        self.generate_data_event.clear()
        self.load_data_event.clear()
        self.game.screens.loading_screen.set_state(False)
        self.game.update_all_uis()
        self.game.player.set_ideal_spawnpoint()

    def regenerate(self, texture_obj):
        self.randomise_seed()
        self.perlin_noise = noise.PerlinNoise()
        self._x = -self.get_width_in_pixels() // 2
        self._y = -self.get_height_in_pixels() // 2
        self.game.camera.x = self.game.camera.y = self.game.camera.velocity_x = self.game.camera.velocity_y = 0
        self.generate(texture_obj)

    def generate_data(self):
        self.game.screens.loading_screen.progress_bar.set_value(0)
        for tile in range(self._width * self._height):
            noise_value = self.perlin_noise.generate(tile % self._width, tile // self._height)
            if noise_value < -1500:
                self._data.append(Textures.WATER)
            elif -1500 <= noise_value < -1000:
                self._data.append(Textures.SAND)
            elif -1000 <= noise_value < -600:
                self._data.append(Textures.DIRT)
            elif -600 <= noise_value < 0:
                self._data.append(Textures.GRASS)
            elif 0 <= noise_value < 500:
                self._data.append(Textures.PLAINS)
            elif 1280 <= noise_value < 1550:
                self._data.append(Textures.LAVA)
            else:
                self._data.append(Textures.COBBLESTONE)

            '''if tile > 0:
                if self._data[tile - offset - 1][0] == self._data[tile - offset][0]:
                    self._data.pop()
                    self._data[tile - offset - 1] = (self._data[tile - offset - 1][0], self._data[tile - offset - 1][1] + 1)
                    offset += 1'''

            self.game.screens.loading_screen.progress_bar.set_value(round((tile + 1) / (self._width * self._height) * 100))
        self.generate_data_event.set()


    def load_data(self, texture_obj):
        for i, tile in enumerate(self._data):
            x: int = (i % self._width) * Texture.SIZE
            y: int = Texture.SIZE * (i // self._width)
            texture_obj.draw(x, y, tile, self._surface)
            self.game.screens.loading_screen.progress_bar.set_value(round((i + 1) / len(self._data) * 100))
        self.load_data_event.set()
        '''index = 0
        for i, tile in enumerate(self._data):
            for _ in range(tile[1]):
                x: int = (index % self._width) * Texture.SIZE
                y: int = Texture.SIZE * (index // self._width)
                texture_obj.draw(x, y, tile[0], self._surface)
                index += 1
            self.game.screens.loading_screen.progress_bar.set_value(round((i + 1) / len(self._data) * 100))'''    

    def update(self, window_obj, player_obj):
        pass

    def break_tile(self, texture_obj):
        tile_x, tile_y = self.game.player.get_selected_tile_x(), self.game.player.get_selected_tile_y()
        if not self.get_dynatile(tile_x, tile_y) and self.get_tile(tile_x, tile_y) in Tiles.BREAKABLE.value:
            self.set_dynatile(tile_x, tile_y, True)
            self.set_tile(tile_x, tile_y, Textures.PLAINS)
            texture_obj.draw(tile_x * Texture.SIZE, tile_y * Texture.SIZE, Textures.PLAINS, self._dynatile_surface)

    def get_tile_pos(self, x, y):
        tile_x = round((x - self._x) / Texture.SIZE)
        tile_y = round((y - self._y) / Texture.SIZE)
        return (tile_x, tile_y)

    def get_strict_tile_pos(self, x, y):
        tile_x = round(x - self._x) // Texture.SIZE
        tile_y = round(y - self._y) // Texture.SIZE
        return (tile_x, tile_y)

    def tile_to_world_pos(self, tile_x, tile_y):
        return (tile_x * Texture.SIZE + self._x, tile_y * Texture.SIZE + self._y)

    def set_tile(self, tile_x, tile_y, tile):
        self._data[tile_x % self._width + tile_y * self._width] = tile
        return self

    def get_tile(self, tile_x, tile_y):
        return self._data[tile_x % self._width + tile_y * self._width]

    def set_data(self, data: list):
        if data:
            self._data = data
        else:
            self._data = Map.DEFAULT
        return self

    def get_data(self):
        return self._data

    def set_dynatile_data(self, dynatile_data: list):
        self._dynatile_data = dynatile_data
        return self

    def get_dynatile_data(self):
        return self._dynatile_data

    def set_dynatile(self, x, y, state):
        self._dynatile_data[y * self._width + x % self._width] = state
        return self

    def get_dynatile(self, x, y):
        return self._dynatile_data[y * self._width + x % self._width]

    def randomise_seed(self):
        self._seed = randint(-Map.SEED_RANGE, Map.SEED_RANGE)
        seed(self._seed)
        return self

    def set_seed(self, _seed):
        self._seed = _seed
        seed(_seed)
        return self

    def get_seed(self):
        return self._seed

    def set_x(self, x):
        self._x = x
        return self

    def get_x(self):
        return self._x

    def set_y(self, y):
        self._y = y
        return self

    def get_y(self):
        return self._y

    def get_width_in_tiles(self):
        return self._width

    def get_width_in_pixels(self):
        return self._width * Texture.SIZE

    def get_height_in_tiles(self):
        return self._height

    def get_height_in_pixels(self):
        return self._height * Texture.SIZE

    def get_surface(self):
        return self._surface

    def get_dynatile_surface(self):
        return self._dynatile_surface
