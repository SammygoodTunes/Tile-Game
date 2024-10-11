
from pygame import image, Surface

from game.data.tiles.tile import Tile
from game.utils.exceptions import InvalidTextureAtlas
from game.utils.logger import logger


class TileManager:
    """
    Class for creating a tile manager.
    """

    SIZE: int = 32

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
        screen.blit(self.atlas,
                    (x, y, self.width, self.height),
                    (TileManager.SIZE * tile.get_xy()[0], TileManager.SIZE * tile.get_xy()[1], TileManager.SIZE, TileManager.SIZE))

    def set_atlas(self, atlas_file: str) -> None:
        """
        Set the texture atlas.
        """
        self.atlas = image.load(atlas_file)
        self.width, self.height = self.atlas.get_rect().size
