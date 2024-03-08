from pygame import draw, image
from .tile_manager import TileManager
from .map_manager import Map
from gui.label import Label
from pygame import mouse
from data.mouse_properties import Mouse
from data.tiles import Tile
from data.items import Items


class World:

    def __init__(self, game):
        self.game = game
        self.tile_manager = TileManager()
        self._map = Map(self.game, 64, 64)

    def initialise(self):
        self.tile_manager.set_atlas(Tile.DEFAULT_ATLAS)
        self._map.regenerate()

    def update(self, window_obj, player_obj):
        self._map.update(window_obj, player_obj)

    def update_ui(self):
        pass

    def draw(self, screen):
        _, _, width, height = screen.get_rect()
        true_x = width / 2 - self.game.camera.x + self._map.get_x()
        true_y = height / 2 - self.game.camera.y + self._map.get_y()

        # Culling applied
        culling_x = self.game.camera.x + self._map.get_width_in_pixels() / 2 - width / 2
        culling_y = self.game.camera.y + self._map.get_height_in_pixels() / 2 - height / 2
        culling_width = width
        culling_height = height
        screen.blit(self._map.get_surface(), (true_x + culling_x, true_y + culling_y, self._map.get_width_in_pixels(), self._map.get_height_in_pixels()), (culling_x, culling_y, culling_width, culling_height))
        screen.blit(self._map.get_dynatile_surface(), (true_x + culling_x, true_y + culling_y, self._map.get_width_in_pixels(), self._map.get_height_in_pixels()), (culling_x, culling_y, culling_width, culling_height))

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
