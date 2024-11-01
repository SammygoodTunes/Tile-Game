"""
Module name: button
"""

from __future__ import annotations
from pygame import mouse, draw, Surface
from pygame.math import clamp
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING: from game.core.window import Window
from game.gui.label import Widget, Label


class Button(Widget):
    """
    Class for creating a button.
    """

    def __init__(self,
                 text: str = "",
                 x: int = 0,
                 y: int = 0,
                 width: int = 500,
                 height: int = 50) -> None:
        super().__init__(x, y, width, height)
        self.MIN_WIDTH = 10
        self.MIN_HEIGHT = 5
        self.validate_dimensions(width, height)
        self.MAX_WIDTH = width
        self.MAX_HEIGHT = height
        self._background_colour = (255, 255, 255)
        self.label = Label(text).set_font_sizes((8, 10, 12))

    def draw(self, window: Window | Surface) -> None:
        if not self._enabled:
            return
        y = 0
        background_colour = (
            self._background_colour[0] // 2,
            self._background_colour[1] // 2,
            self._background_colour[2] // 2
        )
        if not self.is_hovering_over() and self.get_state():
            background_colour = self._background_colour
        if self.is_hovering_over() and mouse.get_pressed(num_buttons=5)[0]:
            y = 3
            background_colour = (
                self._background_colour[0] // 3,
                self._background_colour[1] // 3,
                self._background_colour[2] // 3
            )
        self.label.center_vertically(self._y + y, self._height)
        draw.rect(window, background_colour, (self._x, self._y + y, self._width, self._height), 2, 5)
        if self._width > self.label.get_width():
            self.label.draw(window)

    def resize(self, window: Window) -> None:
        self._width = int(clamp(window.width * 0.25, self.MIN_WIDTH, self.MAX_WIDTH))
        self._height = int(clamp(window.height * 0.1, self.MIN_HEIGHT, self.MAX_HEIGHT))

    def update(self, window: Window) -> None:
        self.label.update(window)
        self.label.center_horizontally(self._x, self._width)

    def is_hovering_over(self) -> bool:
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y <= mouse_y <= self._y + self._height and self._enabled and self._can_interact)

    def set_background_colour(self, background_colour: tuple[int, int, int]) -> Self:
        """
        Set the background colour of the button, then return the button itself.
        """
        self._background_colour = background_colour
        return self

    def get_background_colour(self) -> tuple[int, int, int]:
        """
        Return the background colour of the button.
        """
        return self._background_colour
