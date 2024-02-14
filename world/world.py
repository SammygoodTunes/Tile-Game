from pygame import draw, image
from .texture_manager import Texture
from .map_manager import Map
from gui.label import Label
from pygame import MOUSEBUTTONDOWN
from data.mouse_properties import Mouse


class World:
    DEFAULT_ATLAS: str = "assets/atlas.png"
    CLOUDS_ASSET: str = "assets/clouds.png"

    def __init__(self, game):
        self.game = game
        self.texture = Texture()
        self._map = Map(self.game, 32, 32)

    def initialise(self):
        self.texture.set_atlas(World.DEFAULT_ATLAS)
        self._map.generate()
        self._map.load(self.texture)

    def events(self, e):
        if e.type == MOUSEBUTTONDOWN:
            if e.button == Mouse.LMB:
                self._map.break_tile(self.texture)

    def update(self, window_obj, player_obj):
        self._map.update(window_obj, player_obj)

    def update_ui(self):
        pass

    def draw(self, screen):
        true_x = self.game.width / 2 - self.game.camera.x + self._map.get_x()
        true_y = self.game.height / 2 - self.game.camera.y + self._map.get_y()
        screen.blit(self._map.get_surface(), (true_x, true_y, self._map.get_width_in_pixels(), self._map.get_height_in_pixels()))
        screen.blit(self._map.get_dynatile_surface().convert_alpha(), (true_x, true_y, self._map.get_width_in_pixels(), self._map.get_height_in_pixels()))

    def draw_wireframe(self, screen):
        for x in range(self._map.get_width_in_tiles() + 1):
            draw.line(screen, (200, 200, 200),
                      (self._map.get_x() + x * Texture.SIZE, self._map.get_y()),
                      (self._map.get_x() + x * Texture.SIZE, self._map.get_y() + self._map.get_height_in_pixels()))
        for y in range(self._map.get_height_in_tiles() + 1):
            draw.line(screen, (200, 200, 200),
                      (self._map.get_x(), self._map.get_y() + y * Texture.SIZE),
                      (self._map.get_x() + self._map.get_width_in_pixels(), self._map.get_y() + y * Texture.SIZE))

    def get_map(self):
        return self._map
