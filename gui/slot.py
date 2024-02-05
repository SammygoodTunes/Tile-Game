
from pygame.draw import rect
from pygame import Surface, SRCALPHA
from .widget import Widget
from utils.tools import clamp


class Slot(Widget):

    MIN_SIZE = 25
    MAX_SIZE = 75

    def __init__(self, x, y):
        super().__init__(x, y)
        self._width = 64
        self._height = 64
        self._outline_colour = (25, 25, 25)
        self._inner_colour = (255, 255, 255)
        self._fill_colour = (124, 102, 210)
        self._outline_width = 3
        self._inner_width = 3
        self._fill_alpha = 100
        self._fill_surface = Surface((self._width, self._height), SRCALPHA, 32).convert_alpha()
        self._item_asset = None
        self._item_count = 0

    def draw(self, screen):
        self._fill_surface.fill(self._fill_colour, (0, 0, self._width, self._height))
        self._fill_surface.set_alpha(self._fill_alpha)
        screen.blit(self._fill_surface, (self._x, self._y, self._width, self._height))
        rect(screen, self._outline_colour, (self._x, self._y, self._width, self._height), self._outline_width, 4)
        rect(screen, self._inner_colour, (
                                            self._x + self._outline_width - 1,
                                            self._y + self._outline_width - 1,
                                            self._width - self._outline_width - 1,
                                            self._height - self._outline_width - 1
                                        ), self._inner_width, 4)
        rect(screen, self._outline_colour, (
                                                    self._x + self._outline_width - 1 + self._inner_width - 1,
                                                    self._y + self._outline_width - 1 + self._inner_width - 1,
                                                    self._width - self._outline_width - 1 - self._inner_width - 1,
                                                    self._height - self._outline_width - 1 - self._inner_width - 1
                                                ), self._outline_width, 4)
        if self._item_asset is not None:
            screen.blit(self._item_asset, (0, 0, self._width, self._height))

    def update(self, window):
        self._width = self._height = clamp(window.width * 0.12, Slot.MIN_SIZE, Slot.MAX_SIZE)
        self._fill_surface = Surface((self._width, self._height), SRCALPHA, 32).convert_alpha()
        return self

    def center_horizontally(self, parent_x, parent_width):
        self._x = parent_x + parent_width / 2 - self._width / 2
        return self

    def center_vertically(self, parent_y, parent_height):
        self._y = parent_y + parent_height / 2 - self._height / 2
        return self

    def set_width(self, width):
        self._width = width
        return self

    def get_width(self):
        return self._width

    def set_height(self, height):
        self._height = height
        return self

    def get_height(self):
        return self._height

    def set_inner_colour(self, inner_colour):
        self._inner_colour = inner_colour
        return self

    def get_inner_colour(self):
        return self._inner_colour

    def set_outline_colour(self, outline_colour):
        self._outline_colour = outline_colour
        return self

    def set_inner_width(self, inner_width):
        self._inner_width = inner_width
        return self

    def get_inner_width(self):
        return self._inner_width

    def get_outline_width(self, outline_width):
        self._outline_width = outline_width
        return self
