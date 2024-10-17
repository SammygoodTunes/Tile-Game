"""
Module name: tile_manager

This module is responsible for rendering the tiles to the map surface.
"""

from pygame import image, Surface

from game.data.properties.tile_properties import TileProperties
from game.data.tiles.tile import Tile
from game.utils.exceptions import InvalidTextureAtlas


class TileManager:
    """
    Class for creating a tile manager.
    """

    def __init__(self) -> None:
        self.atlas = image.load(Tile.DEFAULT_ATLAS)
        self.width, self.height = self.atlas.get_rect().size

    def draw(self, x: int, y: int, tile: Tile | int, screen: Surface) -> None:
        """
        Draw a tile to the screen.
        """
        if self.atlas is None:
            raise InvalidTextureAtlas
        if isinstance(tile, int):
            tile = Tile().decompress(tile)
        screen.blit(self.atlas,(x, y, self.width, self.height),(
            TileProperties.TILE_SIZE * tile.get_xy()[0],
            TileProperties.TILE_SIZE * tile.get_xy()[1],
            TileProperties.TILE_SIZE,
            TileProperties.TILE_SIZE))

    def set_atlas(self, atlas_file: str) -> None:
        """
        Set the texture atlas.
        """
        self.atlas = image.load(atlas_file)
        self.width, self.height = self.atlas.get_rect().size
