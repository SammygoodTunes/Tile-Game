"""
Module name: select_list
"""

from __future__ import annotations
from numpy import ceil
from pygame import Surface
from pygame import mouse, MOUSEBUTTONUP
from pygame.draw import polygon
from pygame.event import Event
from pygame.math import clamp
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING: from game.core.window import Window
from game.data.states.mouse_states import MouseStates
from game.gui.inputbox import InputBox
from game.gui.label import Label
from game.gui.widget import Widget


class SelectBox(Widget):
    """
    Class for creating a select box.
    """

    MIN_VALUE_HEIGHT = 10
    MAX_VALUE_HEIGHT = 50
    MIN_ARROW_WIDTH = 4
    MAX_ARROW_WIDTH = 15
    ARROW_X_OFFSET = 10

    def __init__(self,
                 x: int = 0,
                 y: int = 0,
                 width: int = 800,
                 height: int = 50,
                 tooltip_text: str = '') -> None:
        super().__init__(x, y, width, height)
        self.MIN_WIDTH = 25
        self.MIN_HEIGHT = 10
        self.validate_dimensions(width, height)
        self._display_box = (InputBox(width=width, height=height, tooltip_text=tooltip_text)
                             .set_read_only(True)
                             .set_text_colour((255, 255, 0))
                             .set_border_colour((255, 255, 255)))
        self.set_width(width).set_height(height)
        self._values = []
        self._current_index = 0
        self._open = False
        self._arrow_width = SelectBox.MAX_ARROW_WIDTH
        self._arrow_height = self._arrow_width / 2
        self._arrow_colour = (255, 255, 255)
        self._arrow_y_offset = 0
        self._value_surface = Surface((0, 0))
        self._value_slot_height = 0
        self._has_selected = False

    def draw(self, window: Window | Surface) -> None:
        """
        Draw the select box and its components.
        """
        if not self._enabled:
            return
        self._arrow_colour = (255, 255, 255)
        self._display_box.set_border_colour(self._arrow_colour)
        if self._open:
            self._arrow_colour = (120, 120, 120)
            self._display_box.set_border_colour(self._arrow_colour)
        elif self.is_hovering_over():
            self._arrow_colour = (180, 180, 180)
            self._display_box.set_border_colour((255, 255, 255))

        polygon(window.screen, self._arrow_colour, (
            (
                self._x + self._width - (SelectBox.ARROW_X_OFFSET + self._arrow_width),
                self._y + self._height // 2 - self._arrow_height // 2 + self._arrow_y_offset
            ),
            (
                self._x + self._width - SelectBox.ARROW_X_OFFSET,
                self._y + self._height // 2 - self._arrow_height // 2 + self._arrow_y_offset
            ),
            (
                self._x + self._width - SelectBox.ARROW_X_OFFSET - self._arrow_width // 2,
                self._y + self._height // 2 - self._arrow_height // 2 + self._arrow_height + self._arrow_y_offset
            ),
            (
                self._x + self._width - SelectBox.ARROW_X_OFFSET - ceil(self._arrow_width / 2),
                self._y + self._height // 2 - self._arrow_height // 2 + self._arrow_height + self._arrow_y_offset
            ),
        ))
        self.update(window)
        self._display_box.draw(window.screen)

    def draw_value_list(self, window: Window) -> None:
        """
        Draw the select box's value list and its components.
        This is used independently to the draw method, to handle the rendering priority independent to the actual
        select box rendering priority.
        """
        if not self._open:
            return
        self._value_surface = Surface((self._width + 2, self._value_slot_height * len(self._values) + 2))
        self._value_surface.fill((0, 0, 0))
        window.screen.blit(self._value_surface, (self._x - 2, self._y + self._height))
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
        Handle the select box events.
        """
        if not self._can_interact or not self._enabled:
            return
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

    def resize(self, window: Window) -> None:
        self._width = int(clamp(window.width * 0.4, self.MIN_WIDTH, self.MAX_WIDTH))
        self._height = int(clamp(window.height * 0.1, self.MIN_HEIGHT, self.MAX_HEIGHT))

    def update(self, window: Window) -> None:
        if not self._enabled:
            return
        self._display_box.update(window)
        if len(self._values):
            self._display_box.set_text(self._values[self._current_index])
        self._display_box.center(self._x, self._y, self._width, self._height)
        self._arrow_width = int(clamp(self._width * 0.05, SelectBox.MIN_ARROW_WIDTH, SelectBox.MAX_ARROW_WIDTH))
        self._arrow_height = self._arrow_width / 2
        self._value_slot_height = int(clamp(
            self._height * 0.5,
            SelectBox.MIN_VALUE_HEIGHT,
            SelectBox.MAX_VALUE_HEIGHT)
        )

    def set_open(self, state: bool) -> Self:
        """
        Set the open state of the select box (visibility of the select box's value list), then return the select box
        itself.
        """
        self._open = state
        return self

    def is_open(self) -> bool:
        """
        Return True if the select box is open (and values are visible).
        """
        return self._open

    def is_hovering_over(self) -> bool:
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y <= mouse_y <= self._y + self._height + (self._value_slot_height * len(self._values) if self._open else 0) and
                self._enabled)

    def is_hovering_over_display_box(self):
        """
        Return whether the user's mouse cursor is hovering over the select box's display box.
        """
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y <= mouse_y <= self._y + self._height and self._enabled)

    def is_hovering_over_value_list(self):
        """
        Return whether the user's mouse cursor is hovering over the select box's value list.
        """
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y + self._height
                <= mouse_y <=
                self._y + self._height + self._value_slot_height * len(self._values) and
                self._open and self._enabled)

    def is_hovering_over_value(self, index: int):
        """
        Return whether the user's mouse cursor is hovering over the provided select box value by index.
        """
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x - 2 <= mouse_x <= self._x + self._width and
                self._y + self._height + self._value_slot_height * index + 2
                <= mouse_y <
                self._y + self._height + self._value_slot_height * (index + 1) + 2 and
                self._open and self._enabled)

    def is_selected_value(self, index: int):
        """
        Return whether the provided select box value by index has been selected.
        """
        return self.is_hovering_over_value(index) and mouse.get_pressed(num_buttons=5)[0]

    def set_values(self, values: list[str]) -> Self:
        """
        Set the select box's values, then return the select box itself.
        """
        self._values = values
        return self

    def get_values(self) -> list[str]:
        """
        Return the select box's values.
        """
        return self._values

    def set_current_index(self, index: int) -> Self:
        """
        Set the select box's current index, then return the select box itself.
        """
        self._current_index = index
        return self

    def get_current_index(self) -> int:
        """
        Return the select box's current index.
        """
        return self._current_index

    def get_selected(self) -> str:
        """
        Return the select box's current value by its current index.
        """
        return self._values[self._current_index]

    def set_width(self, width: int) -> Self:
        super().set_width(width)
        self._display_box.set_width(width)
        return self

    def set_height(self, height: int) -> Self:
        super().set_height(height)
        self._display_box.set_height(height)
        return self
