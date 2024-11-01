"""
Module name: horizontal_slider
"""

from __future__ import annotations
import pygame
from pygame import Surface
from pygame.event import Event
from pygame.math import clamp
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING: from game.core.window import Window
from game.data.states.mouse_states import MouseStates
from game.gui.label import Label
from game.gui.widget import Widget


class HorizontalSlider(Widget):
    """
    Class for creating a horizontal slider.
    """

    def __init__(self,
                 title: str = "",
                 x: int = 0,
                 y: int = 0,
                 width: int = 350) -> None:
        super().__init__(x, y)
        self.MIN_WIDTH = 25
        self.validate_dimensions(width, 0)
        self.MAX_WIDTH = width
        self._value = 50
        self._min_value = 0
        self._max_value = 100
        self._bar_colour = (255, 255, 255)
        self._bar_width = 3
        self._button_colour = (255, 255, 255)
        self._button_radius = 10
        self._button_radius_hovered = 12
        self._button_held = False
        self.title_label = Label(title, y=self._y - 40).set_font_sizes((8, 8, 10))
        self.value_label = Label(f"{self._value}", self._x + self._width + 35, self._y - 13).set_font_sizes((7, 8, 8))

    def draw(self, window: Window | Surface) -> None:
        radius: int = self._button_radius_hovered if self.is_hovering_over_button() or self._button_held else self._button_radius
        button_colour = (
            self._button_colour[0] // 2,
            self._button_colour[1] // 2,
            self._button_colour[2] // 2
        ) if self._button_held else self._button_colour

        pygame.draw.line(
            window,
            self._bar_colour,
            (self._x - self._button_radius_hovered, self._y),
            (self._x + self.get_step_in_pixels() * (self._value - self._min_value) - radius, self._y),
            width=self._bar_width
        )
        pygame.draw.line(
            window,
            self._bar_colour,
            (self._x + self.get_step_in_pixels() * (self._value - self._min_value) + radius, self._y),
            (self._x + self._width + self._button_radius_hovered, self._y),
            width=self._bar_width
        )
        pygame.draw.circle(
            window,
            button_colour,
            (self._x + self.get_step_in_pixels() * (self._value - self._min_value), self._y),
            radius=radius,
            width=4)
        self.title_label.draw(window)
        self.value_label.draw(window)

        if not self._button_held:
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self._value = clamp(
            round((mouse_x - self._x) // self.get_step_in_pixels()) + self._min_value,
            self._min_value,
            self._max_value
        )

    def events(self, e: Event) -> None:
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == MouseStates.LMB:
                self._button_held = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == MouseStates.LMB:
                if self.is_hovering_over_button():
                    self._button_held = True
                if self.is_hovering_over() and not self._button_held:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self._value = int(clamp(
                        round((mouse_x - self._x) // self.get_step_in_pixels()) + self._min_value,
                        self._min_value,
                        self._max_value
                    ))
        elif e.type == pygame.MOUSEWHEEL and self.is_hovering_over():
            self._value = int(clamp(self._value + e.y, self._min_value, self._max_value))
        self.value_label.set_text(f'{self._value}')

    def resize(self, window: Window) -> None:
        self._button_radius = int(clamp(window.width * 0.04, 2, 10))
        self._button_radius_hovered = self._button_radius + 2
        self._width = int(clamp(window.width * 0.2, self.MIN_WIDTH, self.MAX_WIDTH))
        self._height = self._bar_width + self._button_radius_hovered

    def update(self, window: Window) -> None:
        self.title_label.update(window)
        self.value_label.update(window)
        self.title_label.center_horizontally(self._x, self._width)
        self.value_label.set_x(self._x + self._width + 35)
        self.title_label.set_y(self._y - 40)
        self.value_label.set_y(self._y - 13)

    def is_hovering_over_button(self) -> bool:
        """
        Return whether the user's mouse cursor is hovering over the horizontal slider's button or not.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (self._x + self.get_step_in_pixels() * (self._value - self._min_value) - self._button_radius
                <= mouse_x <=
                self._x + self.get_step_in_pixels() * (self._value - self._min_value) + self._button_radius
                and self._y - self._button_radius <= mouse_y <= self._y + self._button_radius
                and self._enabled)

    def is_hovering_over(self) -> bool:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width
                and self._y - self._button_radius <= mouse_y <= self._y + self._bar_width + self._button_radius
                and self._enabled)

    def get_bar_width(self) -> int:
        """
        Return the width of the horizontal slider's bar.
        """
        return self._bar_width

    def set_title(self, title: str) -> Self:
        """
        Set the title's text of the horizontal slider, then return the horizontal slider itself.
        """
        self.title_label.set_text(title)
        return self

    def get_title(self) -> str:
        """
        Return the title label's text of the horizontal slider.
        """
        return self.title_label.get_text()

    def set_value_text(self, text: str) -> Self:
        """
        Set the value label's text of the horizontal slider, then return the horizontal slider itself.
        """
        self.value_label.set_text(text)
        return self

    def get_value_text(self) -> str:
        """
        Return the value label's text of the horizontal slider.
        """
        return self.value_label.get_text()

    def set_value(self, value: int) -> Self:
        """
        Set the value of the horizontal slider, then return the horizontal slider itself.
        """
        self._value = value
        return self

    def get_value(self) -> int:
        """
        Return the value of the horizontal slider.
        """
        return self._value

    def set_value_bounds(self, min_value: int | None = None, max_value: int | None = None) -> Self:
        """
        Set the value bounds of the horizontal slider (min/max value), then return the horizontal slider itself.
        """
        if min_value is not None:
            self._min_value = min_value
        if max_value is not None:
            self._max_value = max_value
        return self

    def get_value_bounds(self) -> tuple[int, int]:
        """
        Return the value bounds of the horizontal slider (min/max value).
        """
        return self._min_value, self._max_value

    def button_held(self, state: bool) -> Self:
        """
        Set whether the horizontal slider's button is held or not, then return the horizontal slider itself.
        """
        self._button_held = state
        return self

    def is_button_held(self) -> bool:
        """
        Return the held state of the horizontal slider's button.
        """
        return self._button_held

    def get_step_in_pixels(self) -> float:
        """
        Return the number of pixels needed to move the horizontal slider's button from one value to the next.
        """
        return self._width / (self._max_value - self._min_value)

    def set_state(self, state: bool) -> Self:
        super().set_state(state)
        self._button_held = False
        return self
