"""
Module name: widget

This module defines the bass class for all GUI widgets.
"""

from __future__ import annotations
from pygame import Surface
from pygame.event import Event
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING: from game.core.window import Window
from game.utils.logger import logger


class Widget:
    """
    Class for creating a widget.
    """

    MIN_WIDTH = 0
    MAX_WIDTH = 0
    MIN_HEIGHT = 0
    MAX_HEIGHT = 0

    def __init__(self, x: int, y: int, width: int = 0, height: int = 0) -> None:
        self._x: int = x
        self._y: int = y
        self._width: int = width
        self._height: int = height
        self._transparency: float = 1.0
        self._enabled: bool = True
        self._can_interact: bool = True

    @classmethod
    def validate_dimensions(cls, width: int, height: int) -> None:
        """
        Test a widget's dimensions.
        """
        assert width >= cls.MIN_WIDTH, f'Invalid width for {cls.__name__} ({width} < {cls.MIN_WIDTH}'
        assert height >= cls.MIN_HEIGHT, f'Invalid height for {cls.__name__} ({height} < {cls.MIN_HEIGHT}'

    def events(self, e: Event) -> None:
        """
        Handle the widget events.
        """
        ...

    def resize(self, window: Window) -> None:
        """
        Resize the widget based on the screen dimensions.
        """

    def update(self, window: Window) -> None:
        """
        Update the widget and its components.
        """
        ...

    def draw(self, window: Window | Surface) -> None:
        """
        Draw the widget and its components.
        """
        ...

    def is_hovering_over(self) -> bool:
        """
        Return whether the user's mouse cursor is hovering over the widget or not.
        """
        ...

    def set_x(self, x: int) -> Self:
        """
        Set the x position of the widget, then return the widget itself.
        """
        self._x = x
        return self

    def get_x(self) -> int:
        """
        Return the x position of the widget.
        """
        return self._x

    def set_y(self, y: int) -> Self:
        """
        Set the y position of the widget, then return the widget itself.
        """
        self._y = y
        return self

    def get_y(self) -> int:
        """
        Return the y position of the widget.
        """
        return self._y

    def offset_x(self, offset_x: int) -> Self:
        """
        Add an offset to the x position of the widget, then return the widget itself.
        """
        self._x += offset_x
        return self

    def offset_y(self, offset_y: int) -> Self:
        """
        Add an offset to the y position of the widget, then return the widget itself.
        """
        self._y += offset_y
        return self

    def offset(self, offset_x: int, offset_y: int) -> Self:
        """
        Add an offset to the x and y positions of the widget, then return the widget itself.
        """
        self._x += offset_x
        self._y += offset_y
        return self

    def center_horizontally(self, parent_x: int, parent_width: int) -> Self:
        """
        Center the widget horizontally relative to the specified parent, then return the widget itself.
        """
        self._x = round(parent_x + parent_width / 2 - self._width / 2)
        return self

    def center_vertically(self, parent_y: int, parent_height: int) -> Self:
        """
        Center the widget vertically relative to the specified parent, then return the widget itself.
        """
        self._y = round(parent_y + parent_height / 2 - self._height / 2)
        return self

    def center(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int) -> Self:
        """
        Center the widget on both axes relative to the specified parent, then return the widget itself.
        """
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        return self

    def center_with_offset(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int, x: int, y: int) -> Self:
        """
        Center the widget with and offset it by x and y relative to the specified parent, then return the widget itself.
        """
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        return self

    def set_width(self, width: int) -> Self:
        """
        Set the width of the widget, then return the widget itself.
        """
        self.MAX_WIDTH = width
        return self

    def get_width(self) -> int:
        """
        Get the width of the widget.
        """
        return self._width

    def set_height(self, height: int) -> Self:
        """
        Set the height of the widget, then return the widget itself.
        """
        self.MAX_HEIGHT = height
        return self

    def get_height(self) -> int:
        """
        Get the height of the widget.
        """
        return self._height

    def set_transparency(self, transparency: float) -> Self:
        """
        Set the widget's transparency, then return the widget itself.
        """
        self._transparency = transparency
        return self

    def get_transparency(self) -> float:
        """
        Return the widget's transparency.
        """
        return self._transparency

    def set_state(self, state: bool) -> Self:
        """
        Set the widget's visibility and interactivity state, then return the widget itself.
        """
        self._enabled = state
        logger.debug(f'Setting {__class__.__name__} to {state}')
        return self

    def get_state(self) -> bool:
        """
        Return the widget's visibility and interactivity state.
        """
        return self._enabled

    def set_interact(self, state: bool) -> Self:
        """
        Set whether the widget is interactable or not, independent to its visibility, then return the widget itself.
        """
        self._can_interact = state
        return self

    def can_interact(self) -> bool:
        """
        Return whether the widget can be interacted with or not, independent to its visibility.
        """
        return self._can_interact

