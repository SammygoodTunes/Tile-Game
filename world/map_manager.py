from .texture_manager import Textures, Texture
from utils.exceptions import InvalidMapData
from utils.tools import clamp
from random import randint, seed, random
from .synth import noise
import pygame
from threading import Thread, Event


class Map:
    DEFAULT = ([Textures.GRASS if randint(0, 8) == 0 else Textures.PLAINS for x in range(2048)]
               + [Textures.DIRT if randint(0, 10) == 0 else Textures.PLAINS for x in range(1024)]
               + [Textures.DIRT if randint(0, 8) == 0 else Textures.COBBLESTONE for x in range(2048)])

    SEED_RANGE = 2**16

    def __init__(self, game, width, height):
        self.game = game
        self._data: list = list()
        self._seed = 0
        self._x = -width * Texture.SIZE // 2
        self._y = -height * Texture.SIZE // 2
        self._width = width
        self._height = height
        self._surface = None
        self.randomise_seed()
        self.perlin_noise = noise.PerlinNoise()

    def generate(self):
        self._data.clear()
        self._surface = pygame.Surface((self._width * Texture.SIZE, self._height * Texture.SIZE))
        self.game.screens.loading_screen.set_state(True)
        offset = 0
        event = Event()
        update_thread = Thread(target=self.game.screens.loading_screen.independant_update, args=(event, self.game, "Generating map..."))
        update_thread.start()
        print(f"Generating {self._width * self._height} tiles with seed {self._seed}...")
        for tile in range(self._width * self._height):
            noise_value = self.perlin_noise.generate(tile % self._width, tile // self._height)
            if noise_value < -80:
                self._data.append((Textures.WATER, 1))
            elif -80 <= noise_value < -48:
                self._data.append((Textures.SAND, 1))
            elif -48 <= noise_value < -24:
                self._data.append((Textures.DIRT, 1))
            elif -24 <= noise_value <= 20:
                self._data.append((Textures.GRASS, 1))
            elif 20 <= noise_value <= 35:
                self._data.append((Textures.PLAINS, 1))
            elif 100 <= noise_value <= 128:
                self._data.append((Textures.LAVA, 1))
            else:
                self._data.append((Textures.COBBLESTONE, 1))

            if tile > 0:
                if self._data[tile - offset - 1][0] == self._data[tile - offset][0]:
                    self._data.pop()
                    self._data[tile - offset - 1] = (self._data[tile - offset - 1][0], self._data[tile - offset - 1][1] + 1)
                    offset += 1

            self.game.screens.loading_screen.progress_bar.set_value(round((tile + 1) / (self._width * self._height) * 100))

        print(f"Map data length: {len(self._data)}")
        event.set()
        self.game.screens.loading_screen.progress_bar.set_value(0)

    def regenerate(self, texture_obj):
        self.randomise_seed()
        self.perlin_noise = noise.PerlinNoise()
        self._x = -self.get_width_in_pixels() // 2
        self._y = -self.get_height_in_pixels() // 2
        self.game.camera.x = self.game.camera.y = self.game.camera.velocity_x = self.game.camera.velocity_y = 0
        self.generate()
        self.load(texture_obj)

    def load(self, texture_obj):
        event = Event()
        update_thread = Thread(target=self.game.screens.loading_screen.independant_update, args=(event, self.game, "Loading map..."))
        update_thread.start()

        index = 0
        for i, tile in enumerate(self._data):
            for _ in range(tile[1]):
                x: int = (index % self._width) * Texture.SIZE
                y: int = Texture.SIZE * (index // self._width)
                texture_obj.draw(x, y, tile[0], self._surface)
                index += 1
            self.game.screens.loading_screen.progress_bar.set_value(round((i + 1) / len(self._data) * 100))    
        event.set()

        if not self._data:
            raise InvalidMapData
        self.game.screens.loading_screen.set_state(False)
        self.game.update_all_uis()

    def update(self, window_obj, player_obj):
        '''d: float = window_obj.clock.get_time() / 1000.0
        if player_obj.is_near_left_edge():
            if self._x < 0:
                self._x = self._x + player_obj.speed * d * player_obj.is_moving_left()
            else:
                self._x = clamp(self._x, -self._width * Texture.SIZE, 0)
        if player_obj.is_near_right_edge():
            if self._x + self._width * Texture.SIZE > window_obj.width:
                self._x = self._x - player_obj.speed * d * player_obj.is_moving_right()
            else:
                self._x = clamp(self._x, -self._width * Texture.SIZE + window_obj.width, 0)
        if player_obj.is_near_top_edge():
            if self._y < 0:
                self._y = self._y + player_obj.speed * d * player_obj.is_moving_up()
            else:
                self._y = clamp(self._y, -self._height * Texture.SIZE, 0)
        if player_obj.is_near_bottom_edge():
            if self._y + self._height * Texture.SIZE > window_obj.height:
                self._y = self._y - player_obj.speed * d * player_obj.is_moving_down()
            else:
                self._y = clamp(self._y, -self._height * Texture.SIZE + window_obj.height, 0)'''

    def set_data(self, data: list):
        if data:
            self._data = data
        else:
            self._data = Map.DEFAULT
        return self

    def get_data(self):
        return self._data

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
