import pygame
from pygame import mouse, draw, event, key, MOUSEBUTTONDOWN, KEYDOWN, K_BACKSPACE, SRCALPHA
from pygame.math import clamp
from string import printable
from typing import Self

from game.gui.label import Widget, Label
from game.data.mouse_properties import Mouse
from game.utils.logger import logger


class InputBox(Widget):
    """
    Class for creating an input box.
    """

    MIN_WIDTH = 25
    MAX_WIDTH = 500
    MIN_HEIGHT = 25
    MAX_HEIGHT = 50

    def __init__(self, text: str = "", x: int = 0, y: int = 0, width: int = 200, height: int = 50) -> None:
        super().__init__(x, y)
        self._width = width
        self._height = height
        self._selected = False
        self._background_colour = (255, 255, 255)
        self._text_value = text
        self._placeholder_label = Label("", 5, 0).set_font_sizes((8, 10, 12)).set_colour((200, 200, 200)).set_transparency(0.5)
        self._text_label = Label(self._text_value, 5, 0).set_font_sizes((8, 10, 12))
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def draw(self, screen) -> None:
        """
        Draw the input box and its components.
        """
        draw.rect(screen, self._background_colour, (self._x, self._y, self._width, self._height), 2)
        if self._text_value.strip():
            self._text_label.draw(screen)
        else:
            self._placeholder_label.draw(screen)

    def events(self, e: event.Event) -> None:
        """
        Track the input box events.
        """
        if e.type == MOUSEBUTTONDOWN:
            if e.button == Mouse.LMB:
                self._selected = self.is_hovering_over()
        if e.type == KEYDOWN and self._selected:
            if key.get_pressed()[K_BACKSPACE]:
                self._text_value = self._text_value[:-1]
            elif e.unicode in printable:
                self._text_value += e.unicode
            self._text_label.set_text(self._text_value)

    def update(self, window) -> None:
        """
        Update the input box and its components.
        """
        inputbox_width = clamp(window.width * 0.25, InputBox.MIN_WIDTH, InputBox.MAX_WIDTH)
        inputbox_height = clamp(window.height * 0.1, InputBox.MIN_HEIGHT, InputBox.MAX_HEIGHT)
        self._placeholder_label.set_auto_font_size(window.width, window.height, window.max_width, window.max_height)
        self._placeholder_label.center_vertically(self._y, self._height)
        self._placeholder_label.set_x(self._x + 5)
        self._text_label.set_auto_font_size(window.width, window.height, window.max_width, window.max_height)
        self._text_label.center_vertically(self._y, self._height)
        self._text_label.set_x(self._x + 5)
        self._width = inputbox_width
        self._height = inputbox_height
        self.refresh()

    def refresh(self) -> None:
        """
        Refresh the input box and its components.
        """
        self._placeholder_label.refresh()
        self._text_label.refresh()

    def is_hovering_over(self) -> bool:
        """
        Return whether the user's mouse cursor is hovering over the input box or not.
        """
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y <= mouse_y <= self._y + self._height and self._enabled)

    def is_selected(self) -> bool:
        """
        Return whether the input box is selected or not.
        """

    def center_horizontally(self, parent_x: int, parent_width: int) -> Self:
        """
        Center the input box horizontally relative to the specified parent, then return the input box itself.
        """
        self._x = round(parent_x + parent_width / 2 - self._width / 2)
        self.refresh()
        return self

    def center_vertically(self, parent_y: int, parent_height: int) -> Self:
        """
        Center the input box vertically relative to the specified parent, then return the input box itself.
        """
        self._y = round(parent_y + parent_height / 2 - self._height / 2)
        self.refresh()
        return self

    def center(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int) -> Self:
        """
        Center the input box on both axes relative to the specified parent, then return the input box itself.
        """
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        return self

    def center_with_offset(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int, x: int, y: int) -> Self:
        """
        Center the input box with center() and offset it by x and y relative to the specified parent, then return the
        input box itself.
        """
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        return self

    def set_width(self, width: int) -> Self:
        """
        Set the width of the input box, then return the input box itself.
        """
        self._width = width
        return self

    def get_width(self) -> int:
        """
        Return the width of the input box.
        """
        return self._width

    def set_height(self, height: int) -> Self:
        """
        Set the height of the input box, then return the input box itself.
        """
        self._height = height
        return self

    def get_height(self) -> int:
        """
        Return the height of the input box.
        """
        return self._height

    def set_background_colour(self, background_colour: tuple[int, int, int]) -> Self:
        """
        Set the background colour of the input box, then return the input box itself.
        """
        self._background_colour = background_colour
        return self

    def get_background_colour(self) -> tuple[int, int, int]:
        """
        Return the background colour of the input box.
        """
        return self._background_colour

    def set_placeholder_text(self, placeholder_text: str) -> Self:
        """
        Set the placeholder label text of the input box, then return the input box itself.
        """
        self._placeholder_label.set_text(placeholder_text)
        return self

    def get_placeholder_text(self) -> str:
        """
        Return the placeholder label text.
        """
        return self._placeholder_label.get_text()

    def set_text(self, text: str) -> Self:
        """
        Set the label text of the input box, then return the input box itself.
        """
        self._text_value = text
        return self

    def get_text(self) -> str:
        """
        Return the label text of the input box.
        """
        return self._text_value
