"""
Module name: select_list
"""

from numpy import ceil
from pygame import Surface, MOUSEBUTTONDOWN
from pygame.draw import polygon
from pygame.event import Event
from pygame.math import clamp
from pygame import mouse, MOUSEBUTTONUP
from typing import Self

from game.data.properties.screen_properties import ScreenProperties
from game.data.states.mouse_states import MouseStates
from game.gui.inputbox import InputBox
from game.gui.label import Label
from game.gui.widget import Widget


class SelectList(Widget):
    """
    Class for creating a select list.
    """
    MIN_HEIGHT = 10
    MAX_HEIGHT = 50
    MIN_ARROW_WIDTH = 4
    MAX_ARROW_WIDTH = 15
    ARROW_X_OFFSET = 10

    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__(x, y)
        self._width = 0
        self._height = 0
        self._values = []
        self._current_index = 0
        self._open = False
        self._display_box = InputBox().set_read_only(True).set_text_colour((255, 255, 0)).set_border_colour((255, 255, 255))
        self._arrow_width = SelectList.MAX_ARROW_WIDTH
        self._arrow_height = self._arrow_width / 2
        self._arrow_colour = (255, 255, 255)
        self._arrow_y_offset = 0
        self._value_surface = Surface((0, 0))
        self._value_slot_height = self._height
        self._has_selected = False

    def draw(self, window) -> None:
        """
        Draw the select list and its components.
        """
        if self._open:
            self._arrow_colour = (120, 120, 120)
            self._display_box.set_border_colour(self._arrow_colour)
        elif self.is_hovering_over():
            self._arrow_colour = (180, 180, 180)
            self._display_box.set_border_colour((255, 255, 255))
        else:
            self._arrow_colour = (255, 255, 255)
            self._display_box.set_border_colour(self._arrow_colour)

        self._display_box.update(window)
        self._display_box.draw(window.screen)
        polygon(window.screen, self._arrow_colour, (
            (
                self._x + self._width - (SelectList.ARROW_X_OFFSET + self._arrow_width),
                self._y + self._height // 2 - self._arrow_height // 2 + self._arrow_y_offset
            ),
            (
                self._x + self._width - SelectList.ARROW_X_OFFSET,
                self._y + self._height // 2 - self._arrow_height // 2 + self._arrow_y_offset
            ),
            (
                self._x + self._width - SelectList.ARROW_X_OFFSET - self._arrow_width // 2,
                self._y + self._height // 2 - self._arrow_height // 2 + self._arrow_height + self._arrow_y_offset
            ),
            (
                self._x + self._width - SelectList.ARROW_X_OFFSET - ceil(self._arrow_width / 2),
                self._y + self._height // 2 - self._arrow_height // 2 + self._arrow_height + self._arrow_y_offset
            ),
        ))
        if not self._open:
            return
        self._value_surface = Surface((self._width, self._value_slot_height * len(self._values)))
        self._value_surface.fill((0, 0, 0))
        self._value_surface.set_alpha(ScreenProperties.ALPHA)
        window.screen.blit(self._value_surface, (self._x, self._y + self._height))
        for i, value in enumerate(self._values):
            label = Label(x=self._x + 5, text=value).set_colour((150, 150, 150)).set_font_sizes((8, 10, 12))
            label.update(window)
            label.center_vertically(self._y + self._height + self._value_slot_height * i, self._value_slot_height)
            if self.is_hovering_over_value(i):
                label.set_colour((255, 255, 255))
            if self.is_selected_value(i):
                self._has_selected = True
                self._current_index = i
            label.draw(window.screen)

    def events(self, e: Event) -> None:
        """
        Handle the select list events.
        """
        if e.type == MOUSEBUTTONUP:
            if e.button == MouseStates.LMB:
                if self._has_selected:
                    self._has_selected = False
                    self._open = False
                self._open = self.is_hovering_over() if not self._open else self.is_hovering_over_value_list()
        self._arrow_y_offset = self._open * 3

        if not len(self._values) or self._has_selected:
            return
        self._display_box.set_text(self._values[self._current_index])

    def update(self, window) -> None:
        """
        Update the select list and its components.
        """
        self._display_box.update(window)
        self._display_box.center(self._x, self._y, self._width, self._height)
        self._width, self._height = self._display_box.get_width(), self._display_box.get_height()
        self._arrow_width = int(clamp(self._width * 0.05, SelectList.MIN_ARROW_WIDTH, SelectList.MAX_ARROW_WIDTH))
        self._arrow_height = self._arrow_width / 2
        self._value_slot_height = int(clamp(self._height * 0.5, SelectList.MIN_HEIGHT, SelectList.MAX_HEIGHT))
        if not len(self._values):
            return
        self._display_box.set_text(self._values[self._current_index])

    def is_open(self) -> bool:
        """
        Return True if the select list is open (and values are visible).
        """
        return self._open

    def is_hovering_over(self) -> bool:
        """
        Return whether the user's mouse cursor is hovering over the select list or not.
        """
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y <= mouse_y <= self._y + self._height + (self._value_slot_height * len(self._values) if self._open else 0) and
                self._enabled)

    def is_hovering_over_display_box(self):
        """
        Return whether the user's mouse cursor is hovering over the select list's display box.
        """
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y <= mouse_y <= self._y + self._height and self._enabled)

    def is_hovering_over_value_list(self):
        """
        Return whether the user's mouse cursor is hovering over the select list's value list.
        """
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y + self._height
                <= mouse_y <=
                self._y + self._height + self._value_slot_height * len(self._values) and
                self._open and self._enabled)

    def is_hovering_over_value(self, index: int):
        """
        Return whether the user's mouse cursor is hovering over the provided select list value by index.
        """
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y + self._height + self._value_slot_height * index
                <= mouse_y <
                self._y + self._height + self._value_slot_height * (index + 1) and
                self._open and self._enabled)

    def is_selected_value(self, index: int):
        """
        Return whether the provided select list value by index has been selected.
        """
        return self.is_hovering_over_value(index) and mouse.get_pressed(num_buttons=5)[0]

    def center_horizontally(self, parent_x: int, parent_width: int) -> Self:
        """
        Center the input box horizontally relative to the specified parent, then return the input box itself.
        """
        self._x = round(parent_x + parent_width / 2 - self._width / 2)
        return self

    def center_vertically(self, parent_y: int, parent_height: int) -> Self:
        """
        Center the input box vertically relative to the specified parent, then return the input box itself.
        """
        self._y = round(parent_y + parent_height / 2 - self._height / 2)
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
        Set the select list's width, then return the select list itself.
        """
        self._width = width
        return self

    def get_width(self) -> int:
        """
        Return the select list's width.
        """
        return self._width

    def set_height(self, height: int) -> Self:
        """
        Set the select list's height, then return the select list itself.
        """
        self._height = height
        return self

    def get_height(self) -> int:
        """
        Return the select list's height.
        """
        return self._height

    def set_values(self, values: list[str]) -> Self:
        """
        Set the select list's values, then return the select list itself.
        """
        self._values = values
        return self

    def get_values(self) -> list[str]:
        """
        Return the select list's values.
        """
        return self._values

    def set_current_index(self, index: int) -> Self:
        """
        Set the select list's current index, then return the select list itself.
        """
        self._current_index = index
        return self

    def get_current_index(self) -> int:
        """
        Return the select list's current index.
        """
        return self._current_index

    def get_selected(self) -> str:
        """
        Return the select list's current value by its current index.
        """
        return self._values[self._current_index]
