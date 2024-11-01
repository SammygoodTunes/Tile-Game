"""
Module name: progress_bar
"""

from __future__ import annotations
from pygame import draw, Surface
from pygame.math import clamp
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING: from game.core.window import Window
from game.gui.label import Label
from game.gui.widget import Widget


class ProgressBar(Widget):
    """
    Class for creating a progress bar
    """

    def __init__(self,
                 title: str = '',
                 x: int = 0,
                 y: int = 0,
                 width: int = 800,
                 height: int = 30,
                 value: int = 0,
                 min_value: int = 0,
                 max_value: int = 100) -> None:
        super().__init__(x, y)
        self.MIN_WIDTH = 25
        self.MIN_HEIGHT = 10
        self.validate_dimensions(width, height)
        self.MAX_WIDTH = width
        self.MAX_HEIGHT = height
        self._value = value
        self._min_value = min_value
        self._max_value = max_value
        self._unfilled_colour = (50, 50, 50)
        self._filled_start_colour = (255, 50, 80)
        self._filled_end_colour = (120, 255, 130)
        self.info_label = Label().set_font_sizes((8, 9, 10))
        self.info_label.set_text(title)
        self.progress_label = Label(text=f'{self._value} / {self._max_value}').set_font_sizes((7, 8, 9))

    def draw(self, window: Window | Surface) -> None:
        if not self._enabled:
            return
        self.progress_label.set_text(f'{self._value} / {self._max_value}')
        width = self.progress_label.get_width()
        r_diff = round((self._filled_start_colour[0] - self._filled_end_colour[0]) / self._max_value * self._value)
        g_diff = round((self._filled_start_colour[1] - self._filled_end_colour[1]) / self._max_value * self._value)
        b_diff = round((self._filled_start_colour[2] - self._filled_end_colour[2]) / self._max_value * self._value)
        filled_colour = (
                int(clamp(self._filled_start_colour[0] - r_diff, 0, 255)),
                int(clamp(self._filled_start_colour[1] - g_diff, 0, 255)),
                int(clamp(self._filled_start_colour[2] - b_diff, 0, 255))
            )
        draw.rect(window, self._unfilled_colour, (self._x, self._y, self._width, self._height), border_radius=4)
        draw.rect(
            window,
            filled_colour,
            (self._x, self._y, self._width / self._max_value * self._value, self._height),
            border_radius=4
        )
        draw.rect(
            window,
            (0, 0, 0),
            (self._x - 2, self._y - 2, self._width + 4, self._height + 4),
            width=2,
            border_radius=6
        )
        self.info_label.draw(window)

        if self._width > width:
            self.progress_label.draw(window)

    def update(self, window: Window) -> None:
        if not self._enabled:
            return
        self.info_label.update(window)
        self.progress_label.update(window)
        self._width = int(clamp(window.width * 0.2, self.MIN_WIDTH, self.MAX_WIDTH))
        self._height = int(clamp(window.height * 0.2, self.MIN_HEIGHT, self.MAX_HEIGHT))
        self.info_label.center_with_offset(self._x, self._y, self._width, self._height, 0, - self._height)
        self.progress_label.center(self._x, self._y, self._width, self._height - 2)

    def set_value(self, value: int) -> Self:
        """
        Set the value of the progress bar, then return the progress bar itself.
        """
        self._value = value
        return self

    def get_value(self) -> int:
        """
        Return the value of the progress bar.
        """
        return self._value

    def set_value_bounds(self, min_value: int | None = None, max_value: int | None = None) -> Self:
        """
        Set the value bounds of the progress bar (min/max values), then return the progress bar itself.
        """
        if min_value is not None:
            self._min_value = min_value
        if max_value is not None:
            self._max_value = max_value
        return self

    def get_value_bounds(self) -> tuple[int, int]:
        """
        Return the value bounds of the progress bar (min/max values).
        """
        return self._min_value, self._max_value

    def set_unfilled_colour(self, unfilled_colour: tuple[int, int, int]) -> Self:
        """
        Set the unfilled colour of the progress bar, then return the progress bar itself.
        """
        self._unfilled_colour = unfilled_colour
        return self

    def get_unfilled_colour(self) -> tuple[int, int, int]:
        """
        Return the unfilled colour of the progress bar.
        """
        return self._unfilled_colour

    def set_filled_start_colour(self, filled_start_colour: tuple[int, int, int]) -> Self:
        """
        Set the filled start colour of the progress bar, then return the progress bar itself.
        """
        self._filled_start_colour = filled_start_colour
        return self

    def get_filled_start_colour(self) -> tuple[int, int, int]:
        """
        Return the filled start colour of the progress bar.
        """
        return self._filled_start_colour

    def set_filled_end_colour(self, filled_end_colour: tuple[int, int, int]) -> Self:
        """
        Set the filled end colour of the progress bar, then return the progress bar itself.
        """
        self._filled_end_colour = filled_end_colour
        return self

    def get_filled_end_colour(self) -> tuple[int, int, int]:
        """
        Return the filled end colour of the progress bar.
        """
        return self._filled_end_colour

    def set_title(self, title: str) -> Self:
        """
        Set the title text of the progress bar, then return the progress bar itself.
        """
        self.info_label.set_text(title)
        return self

    def get_title(self) -> str:
        """
        Return the title text of the progress bar.
        """
        return self.info_label.get_text()
