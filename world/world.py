from pygame import draw, image
from .tile_manager import TileManager
from .map_manager import Map
from gui.label import Label
from pygame import mouse
from data.mouse_properties import Mouse


class World:
    DEFAULT_ATLAS: str = "assets/atlas.png"
    CLOUDS_ASSET: str = "assets/clouds.png"

    def __init__(self, game):
        self.game = game
        self.tile_manager = TileManager()
        self._map = Map(self.game, 128, 128)

    def initialise(self):
        self.tile_manager.set_atlas(World.DEFAULT_ATLAS)
        self._map.regenerate(self.tile_manager)

    def update(self, window_obj, player_obj):
        if mouse.get_pressed()[Mouse.LMB - 1]:
                self._map.break_tile(self.tile_manager)

        self._map.update(window_obj, player_obj)

    def update_ui(self):
        pass

    def draw(self, screen):
        true_x = self.game.width / 2 - self.game.camera.x + self._map.get_x()
        true_y = self.game.height / 2 - self.game.camera.y + self._map.get_y()
        screen.blit(self._map.get_surface(), (true_x, true_y, self._map.get_width_in_pixels(), self._map.get_height_in_pixels()))
        screen.blit(self._map.get_dynatile_surface(), (true_x, true_y, self._map.get_width_in_pixels(), self._map.get_height_in_pixels()))

    def draw_wireframe(self, screen):
        for x in range(self._map.get_width_in_tiles() + 1):
            draw.line(screen, (200, 200, 200),
                      (self._map.get_x() + x * TileManager.SIZE, self._map.get_y()),
                      (self._map.get_x() + x * TileManager.SIZE, self._map.get_y() + self._map.get_height_in_pixels()))
        for y in range(self._map.get_height_in_tiles() + 1):
            draw.line(screen, (200, 200, 200),
                      (self._map.get_x(), self._map.get_y() + y * TileManager.SIZE),
                      (self._map.get_x() + self._map.get_width_in_pixels(), self._map.get_y() + y * TileManager.SIZE))

    def get_map(self):
        return self._map
