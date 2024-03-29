
from pygame import draw

from game.data.tiles import Tile
from game.utils.logger import logger
from game.world.map_manager import Map
from game.world.tile_manager import TileManager


class World:
    """
    Class for creating a world.
    """

    def __init__(self):
        self.tile_manager = TileManager()
        self._map = Map(256, 256)
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def initialise(self, game):
        """
        Initialise the world.
        """
        self.tile_manager.set_atlas(Tile.DEFAULT_ATLAS)
        self._map.regenerate(game)

    def update(self, window_obj, player_obj):
        """
        Update the world.
        """
        if not window_obj.paused:
            self._map.update(window_obj, player_obj)

    def update_ui(self):
        """
        Update the world's UI (unused).
        """
        pass

    def draw(self, game):
        """
        Draw the world (map, tiles, etc).
        """
        _, _, width, height = game.screen.get_rect()
        true_x = width / 2 - game.camera.x + self._map.get_x()
        true_y = height / 2 - game.camera.y + self._map.get_y()

        # Culling applied
        '''
        culling_x = self.game.camera.x + self._map.get_width_in_pixels() / 2 - 200
        culling_y = self.game.camera.y + self._map.get_height_in_pixels() / 2 - 200
        culling_width = 400
        culling_height = 400
        screen.blit(self._map.get_surface(), (true_x + culling_x, true_y + culling_y, self._map.get_width_in_pixels(), self._map.get_height_in_pixels()), (culling_x, culling_y, culling_width, culling_height))
        screen.blit(self._map.get_dynatile_surface(), (true_x + culling_x, true_y + culling_y, self._map.get_width_in_pixels(), self._map.get_height_in_pixels()), (culling_x, culling_y, culling_width, culling_height))
        '''
        game.screen.blit(self._map.get_surface(), (true_x, true_y, self._map.get_width_in_pixels(), self._map.get_height_in_pixels()))
        game.screen.blit(self._map.get_dynatile_surface(), (true_x, true_y, self._map.get_width_in_pixels(), self._map.get_height_in_pixels()))

    def draw_wireframe(self, screen):
        """
        Draw the wireframe of the world.
        """
        for x in range(self._map.get_width_in_tiles() + 1):
            draw.line(screen, (200, 200, 200),
                      (self._map.get_x() + x * TileManager.SIZE, self._map.get_y()),
                      (self._map.get_x() + x * TileManager.SIZE, self._map.get_y() + self._map.get_height_in_pixels()))
        for y in range(self._map.get_height_in_tiles() + 1):
            draw.line(screen, (200, 200, 200),
                      (self._map.get_x(), self._map.get_y() + y * TileManager.SIZE),
                      (self._map.get_x() + self._map.get_width_in_pixels(), self._map.get_y() + y * TileManager.SIZE))

    def get_map(self):
        """
        Return the map.
        """
        return self._map
