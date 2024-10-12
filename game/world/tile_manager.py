
from pygame import image, Surface

from game.data.properties.tile_properties import TileProperties
from game.data.tiles.tile import Tile
from game.utils.exceptions import InvalidTextureAtlas


class TileManager:
    """
    Class for creating a tile manager.
    """

    def __init__(self) -> None:
        self.atlas: Surface | None = None
        self.width: int = 0
        self.height: int = 0

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
        self.atlas = image.load(atlas_file).convert_alpha()
        self.width, self.height = self.atlas.get_rect().size
