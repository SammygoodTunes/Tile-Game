"""
Module name: checkbox
"""

from __future__ import annotations
import pygame.time
from pygame.draw import rect as draw_rect
from pygame import mouse, MOUSEBUTTONDOWN, Surface
from typing import Self, TYPE_CHECKING

from pygame.event import Event
from pygame.math import clamp

if TYPE_CHECKING: from game.core.window import Window
from game.data.properties.gui_properties import GuiProperties
from game.data.states.mouse_states import MouseStates
from game.gui.label import Label
from game.gui.widget import Widget


class Checkbox(Widget):
    """
    Class for creating a checkbox.
    """

    def __init__(self,
                 title: str,
                 x: int = 0,
                 y: int = 0,
                 size: int = 20,
                 checked: bool = False) -> None:
        super().__init__(x, y)
        self.MIN_WIDTH = 9
        self.MIN_HEIGHT = self.MIN_WIDTH
        self.validate_dimensions(size, size)
        self.MAX_WIDTH = size
        self.MAX_HEIGHT = self.MAX_WIDTH
        self._checked = checked
        self._colour = (255, 255, 255)
        self._spacing = 8
        self._timer = pygame.time.get_ticks() / 1000.0
        self.title_label = Label(title, self._x + self._width + self._spacing, self._y).set_font_sizes((8, 8, 10))

    def draw(self, window: Window | Surface) -> None:
        timer = pygame.time.get_ticks() / 1000.0 - self._timer
        wh = pygame.display.get_surface().get_height()
        x, y, w, h = self._x + 4, self._y + 4, self._width - 8, self._height - 8

        if timer > GuiProperties.CHECKBOX_CHECK_ANIM_DURATION:
            timer = GuiProperties.CHECKBOX_CHECK_ANIM_DURATION

        draw_rect(window, self._colour, (self._x, self._y, self._width, self._height), width=2, border_radius=2)
        self.title_label.draw(window)

        if self._checked:
            draw_rect(window, self._colour, (
                timer * (x / GuiProperties.CHECKBOX_CHECK_ANIM_DURATION),
                timer * (y / GuiProperties.CHECKBOX_CHECK_ANIM_DURATION),
                timer * (w / GuiProperties.CHECKBOX_CHECK_ANIM_DURATION),
                timer * (h / GuiProperties.CHECKBOX_CHECK_ANIM_DURATION)
            ))
            return
        draw_rect(window, self._colour, (
            x - timer * (x / GuiProperties.CHECKBOX_CHECK_ANIM_DURATION),
            y + timer * ((wh - y) / GuiProperties.CHECKBOX_CHECK_ANIM_DURATION),
            w - timer * (w / GuiProperties.CHECKBOX_CHECK_ANIM_DURATION),
            h - timer * (h / GuiProperties.CHECKBOX_CHECK_ANIM_DURATION)
        ))

    def events(self, e: Event) -> None:
        if e.type == MOUSEBUTTONDOWN:
            if e.button == MouseStates.LMB and self.is_hovering_over():
                self._checked = not self._checked
                self._timer = pygame.time.get_ticks() / 1000.0

    def resize(self, window: Window) -> None:
        self._width = int(clamp(window.width * 0.05, self.MIN_WIDTH, self.MAX_WIDTH))
        self._height = self._width

    def update(self, window: Window) -> None:
        self.title_label.update(window)
        self.title_label.center_horizontally(
            self.title_label.get_width() // 2 + self._x + self._width + self._spacing, self._height
        )
        self.title_label.center_vertically(self._y, self._height)


    def is_hovering_over(self) -> bool:
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width + self._spacing * 2 + self.title_label.get_width() and
                self._y <= mouse_y <= self._y + self._height and self._enabled)

    def set_checked(self, state: bool) -> Self:
        """
        Set the checked state of the checkbox's button, then return the checkbox itself.
        """
        self._checked = state
        return self

    def is_checked(self) -> bool:
        """
        Return the checked state of the checkbox's button.
        """
        return self._checked

    def offset_x(self, offset_x: int) -> Self:
        super().offset_x(offset_x)
        self.title_label.set_x(self.title_label.get_x() + offset_x)
        self.title_label.set_shadow_x_offset(2)
        return self

    def offset_y(self, offset_y: int) -> Self:
        super().offset_y(offset_y)
        self.title_label.set_y(self.title_label.get_y() + offset_y)
        self.title_label.set_shadow_y_offset(2)
        return self
