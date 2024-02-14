
import pygame
from random import randint
from .textures import Textures, Tiles
from utils.exceptions import InvalidTextureAtlas
from utils.tools import error


class Texture:

    SIZE: int = 32

    def __init__(self):
        self.atlas: pygame.image = None
        self.width: int = 0
        self.height: int = 0

    def draw(self, x: int, y: int, texture: Textures, screen: pygame.Surface):
        if self.atlas is None:
            raise InvalidTextureAtlas
        #surface = pygame.Surface((Texture.SIZE, Texture.SIZE))
        screen.blit(self.atlas,
                    (x, y, self.width, self.height),
                    (Texture.SIZE * texture.value[0], Texture.SIZE * texture.value[1], Texture.SIZE, Texture.SIZE))
        # rotated_surface = pygame.transform.rotate(surface, randint(0, 3) * 90)
        # screen.blit(rotated_surface, (x, y, self.width, self.height))

    def set_atlas(self, atlas_file: str):
        self.atlas = pygame.image.load(atlas_file)
        self.width, self.height = self.atlas.get_rect().size
