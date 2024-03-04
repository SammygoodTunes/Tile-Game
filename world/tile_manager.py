
import pygame
from random import randint
from data.tiles import Tiles, TileTypes
from utils.exceptions import InvalidTextureAtlas
from utils.tools import error


class TileManager:

    SIZE: int = 32

    def __init__(self):
        self.atlas: pygame.image = None
        self.width: int = 0
        self.height: int = 0

    def draw(self, x: int, y: int, tile: Tiles, screen: pygame.Surface):
        if self.atlas is None:
            raise InvalidTextureAtlas
        #surface = pygame.Surface((TileManager.SIZE, TileManager.SIZE))
        screen.blit(self.atlas,
                    (x, y, self.width, self.height),
                    (TileManager.SIZE * tile.get_xy()[0], TileManager.SIZE * tile.get_xy()[1], TileManager.SIZE, TileManager.SIZE))
        # rotated_surface = pygame.transform.rotate(surface, randint(0, 3) * 90)
        # screen.blit(rotated_surface, (x, y, self.width, self.height))

    def set_atlas(self, atlas_file: str):
        self.atlas = pygame.image.load(atlas_file)
        self.width, self.height = self.atlas.get_rect().size
