
from pygame import draw
from typing import Self

from game.data.properties.tile_properties import TileProperties
from game.world.map_manager import Map
from game.world.tile_manager import TileManager


class World:
    """
    Class for creating a world.
    """

    def __init__(self) -> None:
        self._map = Map(64, 64)

    def initialise(self) -> None:
        """
        Initialise the world.
        """
        self._map.initialise()

    def create(self, seed) -> None:
        """
        Create the world.
        """
        self._map.regenerate(seed)

    def update(self, window_obj, player_obj) -> None:
        """
        Update the world.
        """
        if not window_obj.paused:
            self._map.update(window_obj, player_obj)

    def update_ui(self) -> None:
        """
        Update the world's UI (unused).
        """
        pass

    def draw(self, game) -> None:
        """
        Draw the world (map, tiles, etc.).
        """
        _, _, width, height = game.screen.get_rect()
        true_x = width // 2 - int(game.client.camera.x) + self._map.get_x()
        true_y = height // 2 - int(game.client.camera.y) + self._map.get_y()

        # Culling applied
        '''
        culling_x = self.game.client.camera.x + self._map.get_width_in_pixels() / 2 - 200
        culling_y = self.game.client.camera.y + self._map.get_height_in_pixels() / 2 - 200
        culling_width = 400
        culling_height = 400
        screen.blit(self._map.get_surface(), (true_x + culling_x, true_y + culling_y, self._map.get_width_in_pixels(), self._map.get_height_in_pixels()), (culling_x, culling_y, culling_width, culling_height))
        screen.blit(self._map.get_dynatile_surface(), (true_x + culling_x, true_y + culling_y, self._map.get_width_in_pixels(), self._map.get_height_in_pixels()), (culling_x, culling_y, culling_width, culling_height))
        '''
        game.screen.blit(self._map.get_surface(), (true_x, true_y, self._map.get_width_in_pixels(), self._map.get_height_in_pixels()))
        game.screen.blit(self._map.get_dynatile_surface(), (true_x, true_y, self._map.get_width_in_pixels(), self._map.get_height_in_pixels()))

    def draw_wireframe(self, screen) -> None:
            """
            Draw the wireframe of the world.
            """
            for x in range(self._map.get_width_in_tiles() + 1):
                draw.line(screen, (200, 200, 200),
                          (self._map.get_x() + x * TileProperties.TILE_SIZE, self._map.get_y()),
                          (self._map.get_x() + x * TileProperties.TILE_SIZE, self._map.get_y() + self._map.get_height_in_pixels()))
            for y in range(self._map.get_height_in_tiles() + 1):
                draw.line(screen, (200, 200, 200),
                          (self._map.get_x(), self._map.get_y() + y * TileProperties.TILE_SIZE),
                          (self._map.get_x() + self._map.get_width_in_pixels(), self._map.get_y() + y * TileProperties.TILE_SIZE))

    def set_map(self, _map: Map) -> Self:
        """
        Set the map, and return the world object itself.
        """
        self._map = _map
        return self

    def get_map(self) -> Map:
        """
        Return the map.
        """
        return self._map
