"""
Module name: button
"""

from pygame import mouse, draw
from pygame.math import clamp
from typing import Self

from game.gui.label import Widget, Label


class Button(Widget):
    """
    Class for creating a button.
    """

    MIN_WIDTH = 25
    MAX_WIDTH = 500
    MIN_HEIGHT = 25
    MAX_HEIGHT = 50

    def __init__(self, text: str = "", x: int = 0, y: int = 0, width: int = 200, height: int = 50) -> None:
        super().__init__(x, y)
        self._width = width
        self._height = height
        self._background_colour = (255, 255, 255)
        self.label = Label(text).set_font_sizes((8, 10, 12))

    def draw(self, screen) -> None:
        """
        Draw the button and its components.
        """
        if not self._enabled:
            return
        y = 0
        if not self.is_hovering_over() and self.get_state():
            background_colour = self._background_colour
        elif self.is_hovering_over() and mouse.get_pressed(num_buttons=5)[0]:
            y = 3
            background_colour = (
                self._background_colour[0] // 3,
                self._background_colour[1] // 3,
                self._background_colour[2] // 3
            )
        else:
            background_colour = (
                self._background_colour[0] // 2,
                self._background_colour[1] // 2,
                self._background_colour[2] // 2
            )

        self.label.center_horizontally(self._x, self._width)
        self.label.center_vertically(self._y + y, self._height)

        draw.rect(screen, background_colour, (self._x, self._y + y, self._width, self._height), 2, 5)
        if self._width > self.label.get_total_width():
            self.label.draw(screen)

    def update(self, window) -> None:
        """
        Update the button and its components.
        """
        button_width = clamp(window.width * 0.25, Button.MIN_WIDTH, Button.MAX_WIDTH)
        button_height = clamp(window.height * 0.1, Button.MIN_HEIGHT, Button.MAX_HEIGHT)
        self.label.update(window)
        self._width = button_width
        self._height = button_height
        self.refresh()

    def refresh(self) -> None:
        """
        Refresh the button's subcomponents.
        """
        self.label.refresh()

    def is_hovering_over(self) -> bool:
        """
        Return whether the user's mouse cursor is hovering over the button or not.
        """
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y <= mouse_y <= self._y + self._height and self._enabled and self._can_interact)

    def center_horizontally(self, parent_x: int, parent_width: int) -> Self:
        """
        Center the button horizontally relative to the specified parent, then return the button itself.
        """
        self._x = round(parent_x + parent_width / 2 - self._width / 2)
        self.refresh()
        return self

    def center_vertically(self, parent_y: int, parent_height: int) -> Self:
        """
        Center the button vertically relative to the specified parent, then return the button itself.
        """
        self._y = round(parent_y + parent_height / 2 - self._height / 2)
        self.refresh()
        return self

    def center(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int) -> Self:
        """
        Center the button on both axes relative to the specified parent, then return the button itself.
        """
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        return self

    def center_with_offset(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int, x: int, y: int) -> Self:
        """
        Center the button with center() and offset it by x and y relative to the specified parent, then return the
        button itself.
        """
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        return self

    def set_width(self, width: int) -> Self:
        """
        Set the width of the button, then return the button itself.
        """
        self._width = width
        return self

    def get_width(self) -> int:
        """
        Return the width of the button.
        """
        return self._width

    def set_height(self, height: int) -> Self:
        """
        Set the height of the button, then return the button itself.
        """
        self._height = height
        return self

    def get_height(self) -> int:
        """
        Return the height of the button.
        """
        return self._height

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
