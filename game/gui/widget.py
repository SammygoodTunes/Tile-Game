
import inspect
from typing import Self

from game.utils.logger import logger


class Widget:
    """
    Class for creating a widget.
    """

    def __init__(self, x: int, y: int) -> None:
        self._x: int = x
        self._y: int = y
        self._colour = (255, 255, 255)
        self._enabled = False
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

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

    def set_state(self, state: bool) -> Self:
        """
        Set the widget's visibility/interactivity.
        """
        self._enabled = state
        logger.debug(
            f'Setting {__class__.__name__} called by {inspect.stack()[1][0].f_locals["self"].__class__.__name__}'
            f' at {inspect.stack()[1].code_context[0].strip()} to {state}'
        )
        return self

    def get_state(self) -> bool:
        """
        Return the state of the widget's visibility/interactivity.
        """
        return self._enabled
