"""
Module name: label
"""

from __future__ import annotations
from pygame import BLEND_ALPHA_SDL2, math, Surface
from pygame.font import Font
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING: from game.core.window import Window
from game.gui.widget import Widget
from game.utils.tools import resource_dir


class Label(Widget):
    """
    Class for creating a label.
    """

    DEFAULT_FONT = resource_dir('game/assets/font.ttf')
    DEFAULT_FONT_SIZE_SMALL = 8
    DEFAULT_FONT_SIZE_NORMAL = 11
    DEFAULT_FONT_SIZE_LARGE = 13

    def __init__(self, text: str = "", x: int = 0, y: int = 0) -> None:
        super().__init__(x, y)
        self.font = Font(Label.DEFAULT_FONT, Label.DEFAULT_FONT_SIZE_NORMAL)
        self._font_size = Label.DEFAULT_FONT_SIZE_NORMAL
        self._font_sizes = (Label.DEFAULT_FONT_SIZE_SMALL, Label.DEFAULT_FONT_SIZE_NORMAL, Label.DEFAULT_FONT_SIZE_LARGE)
        self._text = text
        self._colour = (255, 255, 255)
        self._shadow_x_offset: int = 2
        self._shadow_y_offset: int = 2
        self._shadow_colour = (0, 0, 0)
        self._antialiasing = False

    def draw(self, window: Window | Surface) -> None:
        lines = self._text.replace('\t', ' ' * 4).split('\n')
        for i, line in enumerate(lines):
            text_shadow = self.font.render(line, self._antialiasing, self._shadow_colour)
            text_shadow.set_alpha(int(math.clamp(255 * self._transparency, 0, 255)))
            text = self.font.render(line, self._antialiasing, self._colour)
            text.set_alpha(int(math.clamp(255 * self._transparency, 0, 255)))
            window.blit(
                text_shadow,
                (
                    self._x + self._shadow_x_offset,
                    self._y + self._shadow_y_offset + (i * (self._height - 4))
                ),
                special_flags=BLEND_ALPHA_SDL2
            )
            window.blit(text, (self._x, self._y + (i * (self._height - 4))), special_flags=BLEND_ALPHA_SDL2)

    def update(self, window: Window) -> None:
        self.set_auto_font_size(window.width, window.height, window.max_width, window.max_height)
        self._width = self.font.size(self._text)[0]
        self._height = self.font.size(self._text)[1]

    def set_auto_font_size(self, width: int, height: int, max_width: int, max_height: int) -> Self:
        """
        Set the automatic font size of the label, then return the label itself.
        """
        if width < max_width / 3 and height < max_height / 3:
            self.set_font_size(self._font_sizes[0])
        elif width < max_width / 3 * 2 and height < max_height / 3 * 2:
            self.set_font_size(self._font_sizes[1])
        else:
            self.set_font_size(self._font_sizes[2])
        return self

    def set_font_size(self, font_size: int) -> Self:
        """
        Set the font size of the label, then return the label itself.
        """
        self.font = Font(Label.DEFAULT_FONT, font_size)
        self._font_size = font_size
        return self

    def get_font_size(self) -> int:
        """
        Return the font size of the label.
        """
        return self._font_size

    def set_font_sizes(self, font_sizes: tuple[int, int, int]) -> Self:
        """
        Set the small, medium and large sizes of the label's text, then return the label itself.
        """
        self._font_sizes = font_sizes
        return self

    def get_font_sizes(self) -> tuple[int, int, int]:
        """
        Return the small, medium and large sizes of the label's text.
        """
        return self._font_sizes

    def set_text(self, text: str) -> Self:
        """
        Set the label's text, then return the label itself.
        """
        self._text = text
        self._width = self.font.size(self._text)[0]
        self._height = self.font.size(self._text)[1]
        return self

    def get_text(self) -> str:
        """
        Return the label's text.
        """
        return self._text

    def set_antialiasing(self, state: bool) -> Self:
        """
        Set the antialiasing state of the label, then return the label itself.
        """
        self._antialiasing = state
        return self

    def has_antialiasing(self) -> bool:
        """
        Returns True if the label has antialiasing enabled.
        """
        return self._antialiasing

    def set_colour(self, colour: tuple[int, int, int]) -> Self:
        """
        Set the label's text colour, then return the label itself.
        """
        self._colour = colour
        return self

    def get_colour(self) -> tuple[int, int, int]:
        """
        Return the label's text colour.
        """
        return self._colour

    def set_shadow_x_offset(self, offset) -> Self:
        """
        Set the x offset of the label's shadow, then return the label itself.
        """
        self._shadow_x_offset = offset
        return self

    def get_shadow_x_offset(self) -> int:
        """
        Return the x offset of the label's shadow.
        """
        return self._shadow_x_offset

    def set_shadow_y_offset(self, offset) -> Self:
        """
        Set the y offset of the label's shadow, then return the label itself.
        """
        self._shadow_y_offset = offset
        return self

    def get_shadow_y_offset(self) -> int:
        """
        Return the y offset of the label's shadow.
        """
        return self._shadow_y_offset

    def set_shadow_colour(self, shadow_colour) -> Self:
        """
        Set the label's text shadow colour, then return the label itself.
        """
        self._shadow_colour = shadow_colour
        return self

    def get_shadow_colour(self) -> tuple[int, int, int]:
        """
        Return the label's text shadow colour.
        """
        return self._shadow_colour
