"""
Module name: widget

This module defines the bass class for all GUI widgets.
"""

from typing import Self

from game.utils.logger import logger


class Widget:
    """
    Class for creating a widget.
    """

    def __init__(self, x: int, y: int) -> None:
        self._x: int = x
        self._y: int = y
        self._transparency: float = 1.0
        self._enabled: bool = False

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
        Set the widget's visibility/interactivity, then return the widget itself.
        """
        self._enabled = state
        logger.debug(f'Setting {__class__.__name__} to {state}')
        return self

    def get_state(self) -> bool:
        """
        Return the state of the widget's visibility/interactivity.
        """
        return self._enabled
