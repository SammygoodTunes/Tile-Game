
from pygame import BLEND_ALPHA_SDL2, math
from pygame.font import Font
from typing import Self

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
        self._shadow_x: int = self._x
        self._shadow_y: int = self._y
        self._shadow_colour = (0, 0, 0)
        self._antialiasing = False

    def draw(self, screen) -> None:
        """
        Draw the label and its components.
        """
        lines = self._text.split('\n')
        for i, line in enumerate(lines):
            text_shadow = self.font.render(line, self._antialiasing, self._shadow_colour)
            text_shadow.set_alpha(int(math.clamp(255 * self._transparency, 0, 255)))
            text = self.font.render(line, self._antialiasing, self._colour)
            text.set_alpha(int(math.clamp(255 * self._transparency, 0, 255)))
            screen.blit(text_shadow, (self._shadow_x, self._shadow_y + (i * (self.get_total_height() - 4))), special_flags=BLEND_ALPHA_SDL2)
            screen.blit(text, (self._x, self._y + (i * (self.get_total_height() - 4))), special_flags=BLEND_ALPHA_SDL2)

    def update(self, window) -> None:
        """
        Update the label and its components.
        """
        self.set_auto_font_size(window.width, window.height, window.max_width, window.max_height)
        self.refresh()

    def refresh(self) -> Self:
        """
        Update the shadow's position of the label.
        """
        self._shadow_x = self._x + 2
        self._shadow_y = self._y + 2
        return self

    def center_horizontally(self, parent_x: int, parent_width: int) -> Self:
        """
        Center the label horizontally relative to the specified parent, then return the label itself.
        """
        width, height = self.font.size(self._text)
        self._x = round(parent_x + parent_width // 2 - width // 2)
        self.refresh()
        return self

    def center_vertically(self, parent_y: int, parent_height: int) -> Self:
        """
        Center the label vertically relative to the specified parent, then return the label itself.
        """
        height = self.get_total_height() + 4  # Bad but seems to fix the centering
        self._y = round(parent_y + parent_height // 2 - height // 2)
        self.refresh()
        return self

    def center(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int) -> Self:
        """
        Center the label on both axes relative to the specified parent, then return the label itself.
        """
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        return self

    def center_with_offset(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int, x: int, y: int) -> Self:
        """
        Center the label with center() and offset it by x and y relative to the specified parent, then return the
        label itself.
        """
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        self.refresh()
        return self

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

    def get_total_width(self) -> int:
        """
        Return the total width of the label.
        """
        return self.font.size(self._text)[0]

    def get_total_height(self) -> int:
        """
        Return the total height of the label.
        """
        return self.font.size(self._text)[1]

    def set_text(self, text: str) -> Self:
        """
        Set the label's text, then return the label itself.
        """
        self._text = text
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

    def set_shadow_x(self, shadow_x: int) -> Self:
        """
        Set the label text's shadow's x position, then return the label itself.
        """
        self._shadow_x = shadow_x
        return self

    def set_x(self, x: int) -> Self:
        """
        Set the label text's x position, then return the label itself.
        """
        super().set_x(x)
        self.refresh()
        return self

    def set_y(self, y: int) -> Self:
        """
        Set the label text's y position, then return the label itself.
        """
        super().set_y(y)
        self.refresh()
        return self

    def get_shadow_x(self) -> int:
        """
        Return the label text's shadow's x position.
        """
        return self._shadow_x

    def set_shadow_y(self, shadow_y: int) -> Self:
        """
        Set the label text's shadow's y position, then return the label itself.
        """
        self._shadow_y = shadow_y
        return self

    def get_shadow_y(self) -> int:
        """
        Return the label text's shadow's y position.
        """
        return self._shadow_y

    def set_shadow_x_offset(self, offset) -> Self:
        """
        Set the label text's shadow's x offset, then return the label itself.
        """
        self._shadow_x = self._x + offset
        return self

    def set_shadow_y_offset(self, offset) -> Self:
        """
        Set the label text's shadow's y offset, then return the label itself.
        """
        self._shadow_y = self._y + offset
        return self

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
