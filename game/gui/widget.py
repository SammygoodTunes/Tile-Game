
import inspect

from game.utils.logger import logger


class Widget:
    """
    Class for creating a widget.
    """

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._colour = (255, 255, 255)
        self._enabled = False
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def set_x(self, x):
        """
        Set the x position of the widget, then return the widget itself.
        """
        self._x = x
        return self

    def get_x(self):
        """
        Return the x position of the widget.
        """
        return self._x

    def set_y(self, y):
        """
        Set the y position of the widget, then return the widget itself.
        """
        self._y = y
        return self

    def get_y(self):
        """
        Return the y position of the widget.
        """
        return self._y

    def offset_x(self, offset_x):
        """
        Set the x offset of the widget, then return the widget itself.
        """
        self._x += offset_x
        return self

    def offset_y(self, offset_y):
        """
        Set the y offset of the widget, then return the widget itself.
        """
        self._y += offset_y
        return self

    def offset(self, offset_x, offset_y):
        """
        Set the x and y offsets of the widget, then return the widget itself.
        """
        self._x += offset_x
        self._y += offset_y
        return self

    def set_state(self, state):
        """
        Set the widget's visibility/interactivity.
        """
        self._enabled = state
        logger.debug(
            f'Setting {__class__.__name__} called by {inspect.stack()[1][0].f_locals["self"].__class__.__name__}'
            f' at {inspect.stack()[1].code_context[0].strip()} to {state}'
        )
        return self

    def get_state(self):
        """
        Return the state of the widget's visibility/interactivity.
        """
        return self._enabled
