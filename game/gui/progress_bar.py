
from pygame import draw
from pygame.math import clamp
from typing import Self

from game.gui.label import Label
from game.gui.widget import Widget
from game.utils.logger import logger


class ProgressBar(Widget):
    """
    Class for creating a progress bar
    """

    MIN_WIDTH = 25
    MAX_WIDTH = 500

    def __init__(self, title: str = "",
                 x: int = 0,
                 y: int = 0,
                 value: int = 0,
                 min_value: int = 0,
                 max_value: int = 100) -> None:
        super().__init__(x, y)
        self._width = 0
        self._height = 16
        self._value = value
        self._min_value = min_value
        self._max_value = max_value
        self._unfilled_colour = (50, 50, 50)
        self._filled_start_colour = (255, 50, 80)
        self._filled_end_colour = (120, 255, 130)
        self.info_label = Label().set_font_sizes((8, 9, 10))
        self.info_label.set_text(title)
        self.progress_label = Label(text=f"{self._value}/{self._max_value}").set_font_sizes((7, 8, 9))


    def draw(self, screen) -> None:
        """
        Draw the progress bar and its components.
        """
        width = self.progress_label.font.size(self.progress_label.get_text())[0]
        self.progress_label.set_text(f"{self._value}/{self._max_value}")
        draw.rect(screen, self._unfilled_colour, (self._x, self._y, self._width, self._height), border_radius=4)
        
        filled_colour = (
                int(clamp(self._filled_start_colour[0] - round((self._filled_start_colour[0] - self._filled_end_colour[0]) / self._max_value * self._value), 0, 255)),
                int(clamp(self._filled_start_colour[1] - round((self._filled_start_colour[1] - self._filled_end_colour[1]) / self._max_value * self._value), 0, 255)),
                int(clamp(self._filled_start_colour[2] - round((self._filled_start_colour[2] - self._filled_end_colour[2]) / self._max_value * self._value), 0, 255))
            )
        draw.rect(screen, filled_colour, (self._x, self._y, self._width / self._max_value * self._value, self._height), border_radius=4)
        draw.rect(screen, (0, 0, 0), (self._x - 2, self._y - 2, self._width + 4, self._height + 4), width=2, border_radius=6)

        self.info_label.draw(screen)
        if self._width > width:
            self.progress_label.draw(screen)

    def update(self, window) -> Self:
        """
        Update the progress bar and its components.
        """
        self.info_label.update(window)
        self.progress_label.update(window)
        self._width = clamp(window.width * 0.2, ProgressBar.MIN_WIDTH, ProgressBar.MAX_WIDTH)
        self._height = self.progress_label.font.size(self.progress_label.get_text())[1] + 8
        self.refresh()
        return self

    def refresh(self) -> None:
        """
        Refresh the progress bar and its components.
        """
        height = self.info_label.font.size(self.info_label.get_text())[1]
        self.info_label.center_with_offset(self._x, self._y, self._width, self._height, 0, -height - 8)
        self.progress_label.center(self._x, self._y, self._width, self._height)
        self.info_label.refresh()
        self.progress_label.refresh()

    def center_horizontally(self, parent_x: int, parent_width: int) -> Self:
        """
        Center the progress bar horizontally relative to the specified parent, then return the progress bar itself.
        """
        self._x = round(parent_x + parent_width / 2 - self._width / 2)
        self.refresh()
        return self

    def center_vertically(self, parent_y: int, parent_height: int) -> Self:
        """
        Center the progress bar horizontally relative to the specified parent, then return the progress bar itself.
        """
        self._y = round(parent_y + parent_height / 2 - self._height / 2)
        self.refresh()
        return self

    def center(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int) -> Self:
        """
        Center the progress bar on both axes relative to the specified parent, then return the progress bar itself.
        """
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        return self

    def center_with_offset(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int, x: int, y: int) -> Self:
        """
        Center the progress bar with center() and offset it by x and y relative to the specified parent, then return the
        progress bar itself.
        """
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        return self

    def set_width(self, width: int) -> Self:
        """
        Set the width of the progress bar, then return the progress bar itself.
        """
        self._width = width
        return self

    def get_width(self) -> int:
        """
        Return the width of the progress bar.
        """
        return self._width

    def set_height(self, height: int) -> Self:
        """
        Set the height of the progress bar, then return the progress bar itself.
        """
        self._height = height
        return self

    def get_height(self) -> int:
        """
        Return the height of the progress bar.
        """
        return self._height

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
