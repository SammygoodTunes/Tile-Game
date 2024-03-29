
from pygame import draw
from pygame.math import clamp

from game.gui.label import Label
from game.gui.widget import Widget
from game.utils.logger import logger


class ProgressBar(Widget):
    """
    Class for creating a progress bar
    """

    MIN_WIDTH = 25
    MAX_WIDTH = 500

    def __init__(self, title="", x=0, y=0):
        super().__init__(x, y)
        self._width = 0
        self._height = 16
        self._value = 0
        self._min_value = 0
        self._max_value = 100
        self._unfilled_colour = (50, 50, 50)
        self._filled_start_colour = (255, 130, 120)
        self._filled_end_colour = (120, 255, 130)
        self.info_label = Label().set_font_sizes((8, 9, 10))
        self.info_label.set_text(title)
        self.progress_label = Label(text=f"{self._value}/{self._max_value}").set_font_sizes((7, 8, 9))
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def draw(self, screen):
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

    def update(self, window):
        """
        Update the progress bar and its components.
        """
        self.info_label.update(window)
        self.progress_label.update(window)
        self._width = clamp(window.width * 0.2, ProgressBar.MIN_WIDTH, ProgressBar.MAX_WIDTH)
        self._height = self.progress_label.font.size(self.progress_label.get_text())[1] + 4
        self.refresh()
        return self

    def refresh(self):
        """
        Refresh the progress bar and its components.
        """
        height = self.info_label.font.size(self.info_label.get_text())[1]
        self.info_label.center_with_offset(self._x, self._y, self._width, self._height, 0, -height - 8)
        self.progress_label.center(self._x, self._y, self._width, self._height)
        self.info_label.refresh()
        self.progress_label.refresh()

    def center_horizontally(self, parent_x, parent_width):
        """
        Center the progress bar horizontally relative to the specified parent, then return the progress bar itself.
        """
        self._x = parent_x + parent_width / 2 - self._width / 2
        self.refresh()
        return self

    def center_vertically(self, parent_y, parent_height):
        """
        Center the progress bar horizontally relative to the specified parent, then return the progress bar itself.
        """
        self._y = parent_y + parent_height / 2 - self._height / 2
        self.refresh()
        return self

    def center(self, parent_x, parent_y, parent_width, parent_height):
        """
        Center the progress bar on both axes relative to the specified parent, then return the progress bar itself.
        """
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        return self

    def center_with_offset(self, parent_x, parent_y, parent_width, parent_height, x, y):
        """
        Center the progress bar with center() and offset it by x and y relative to the specified parent, then return the
        progress bar itself.
        """
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        return self

    def set_width(self, width):
        """
        Set the width of the progress bar, then return the progress bar itself.
        """
        self._width = width
        return self

    def get_width(self):
        """
        Return the width of the progress bar.
        """
        return self._width

    def set_height(self, height):
        """
        Set the height of the progress bar, then return the progress bar itself.
        """
        self._height = height
        return self

    def get_height(self):
        """
        Return the height of the progress bar.
        """
        return self._height

    def set_value(self, value):
        """
        Set the value of the progress bar, then return the progress bar itself.
        """
        self._value = value
        return self

    def get_value(self):
        """
        Return the value of the progress bar.
        """
        return self._value

    def set_value_bounds(self, min_value=None, max_value=None):
        """
        Set the value bounds of the progress bar (min/max values), then return the progress bar itself.
        """
        if min_value is not None:
            self._min_value = min_value
        if max_value is not None:
            self._max_value = max_value
        return self

    def get_value_bounds(self):
        """
        Return the value bounds of the progress bar (min/max values).
        """
        return self._min_value, self._max_value

    def set_unfilled_colour(self, unfilled_colour):
        """
        Set the unfilled colour of the progress bar, then return the progress bar itself.
        """
        self._unfilled_colour = unfilled_colour
        return self

    def get_unfilled_colour(self):
        """
        Return the unfilled colour of the progress bar.
        """
        return self._unfilled_colour

    def set_filled_start_colour(self, filled_start_colour):
        """
        Set the filled start colour of the progress bar, then return the progress bar itself.
        """
        self._filled_start_colour = filled_start_colour
        return self

    def get_filled_start_colour(self):
        """
        Return the filled start colour of the progress bar.
        """
        return self._filled_start_colour

    def set_filled_end_color(self, filled_end_colour):
        """
        Set the filled end colour of the progress bar, then return the progress bar itself.
        """
        self._filled_end_colour = filled_end_colour
        return self

    def get_filled_end_colour(self):
        """
        Return the filled end colour of the progress bar.
        """
        return self._filled_end_colour

    def set_title(self, title):
        """
        Set the title text of the progress bar, then return the progress bar itself.
        """
        self.info_label.set_text(title)
        return self

    def get_title(self):
        """
        Return the title text of the progress bar.
        """
        return self.info_label.get_text()
