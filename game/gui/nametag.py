
from pygame import mouse, draw, Surface
from pygame.math import clamp
from typing import Self

from game.gui.label import Widget, Label
from game.utils.logger import logger


class NameTag(Widget):
    """
    Class for creating a nametag.
    """

    def __init__(self, text: str = "", x: int = 0, y: int = 0) -> None:
        super().__init__(x, y)
        self._width = 0
        self._height = 0
        self._faded_surface = Surface((self._width, self._height))
        self._background_colour = (0, 0, 0)
        self.label = Label(text, self._x, self._y).set_font_sizes((8, 9, 10))
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def draw(self, screen) -> None:
        """
        Draw the nametag and its components.
        """
        if not self._enabled:
            return

        screen.blit(self._faded_surface, (self._x - 5, self._y))
        self.label.draw(screen)

    def update(self, window) -> None:
        """
        Update the nametag and its components.
        """
        self.label.set_auto_font_size(window.width, window.height, window.max_width, window.max_height)
        self._width = self.label.get_total_width() + 10
        self._height = self.label.get_total_height() + 5
        self.label.center_vertically(self._y, self._height)
        self._faded_surface = Surface((self._width, self._height))
        self._faded_surface.fill(self._background_colour)
        self._faded_surface.set_alpha(96)
        self.refresh()

    def refresh(self) -> None:
        """
        Refresh the nametag and its components.
        """
        self.label.refresh()

    def is_hovering_over(self) -> bool:
        """
        Return whether the user's mouse cursor is hovering over the nametag or not.
        """
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y <= mouse_y <= self._y + self._height and self._enabled)

    def set_width(self, width: int) -> Self:
        """
        Set the width of the nametag, then return the nametag itself.
        """
        self._width = width
        return self

    def get_width(self) -> int:
        """
        Return the width of the nametag.
        """
        return self._width

    def set_height(self, height: int) -> Self:
        """
        Set the height of the nametag, then return the nametag itself.
        """
        self._height = height
        return self

    def get_height(self) -> int:
        """
        Return the height of the nametag.
        """
        return self._height

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
        """
        Set the state of the nametag and its components, then return the nametag itself.
        """
        super().set_state(state)
        self.label.set_state(state)
        return self
