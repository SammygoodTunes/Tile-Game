"""
Module name: nametag
"""

from __future__ import annotations
from pygame import mouse, Surface
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING: from game.core.window import Window
from game.gui.label import Widget, Label


class NameTag(Widget):
    """
    Class for creating a nametag.
    """

    def __init__(self, text: str = "", x: int = 0, y: int = 0) -> None:
        super().__init__(x, y)
        self._background_colour = (0, 0, 0)
        self.label = Label(text, self._x, self._y).set_font_sizes((8, 9, 10))
        self._faded_surface = Surface((self._width, self._height))
        self._transparency = 0.4

    def draw(self, window: Window | Surface) -> None:
        if not self._enabled:
            return
        print(self._x, self._y)
        window.blit(self._faded_surface, (self._x, self._y))
        self.label.draw(window)

    def update(self, window: Window) -> None:
        self.label.update(window)
        self._width = self.label.get_width() + 5
        self._height = self.label.get_height()
        self.label.center_horizontally(self._x, self._width)
        self.label.center_vertically(self._y, self._height)
        self._faded_surface = Surface((self._width, self._height))
        self._faded_surface.fill(self._background_colour)
        self._faded_surface.set_alpha(round(self._transparency * 255))

    def is_hovering_over(self) -> bool:
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y <= mouse_y <= self._y + self._height and self._enabled)

    def set_background_colour(self, background_colour: tuple[int, int, int]) -> Self:
        """
        Set the background colour of the nametag, then return the nametag itself.
        """
        self._background_colour = background_colour
        return self

    def get_background_colour(self) -> tuple[int, int, int]:
        """
        Return the background colour of the nametag.
        """
        return self._background_colour

    def set_state(self, state: bool) -> Self:
        super().set_state(state)
        self.label.set_state(state)
        return self
