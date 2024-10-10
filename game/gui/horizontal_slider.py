
import pygame
from pygame.math import clamp
from typing import Self

from game.data.states.mouse_states import MouseStates
from game.gui.label import Label
from game.gui.widget import Widget
from game.utils.logger import logger


class HorizontalSlider(Widget):
    """
    Class for creating a horizontal slider.
    """

    MIN_WIDTH = 50
    MAX_WIDTH = 350

    def __init__(self, title: str = "", x: int = 0, y: int = 0) -> None:
        super().__init__(x, y)
        self._width = 0
        self._height = 40 - 13
        self._value = 50
        self._min_value = 0
        self._max_value = 100
        self._bar_colour = (255, 255, 255)
        self._bar_width = 3
        self._button_colour = (255, 255, 255)
        self._button_outline_colour = (240, 240, 240)
        self._button_radius = 10
        self._button_radius_hovered = 12
        self._button_held = False
        self.title_label = Label(title, 0, self._y - 40).set_font_sizes((7, 8, 10))
        self.value_label = Label(f"{self._value}", self._x + self._width + 35, self._y - 13).set_font_sizes((6, 7, 8))
        logger.debug(f'Created {__class__.__name__} with attributes {self.__dict__}')

    def draw(self, screen) -> None:
        """
        Draw the horizontal slider and its components.
        """
        radius: int = self._button_radius_hovered if self.is_hovering_over_button() else self._button_radius
        if self._button_held:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self._value = round((mouse_x - self._x) // self.get_step_in_pixels()) + self._min_value
            self._value = clamp(self._value, self._min_value, self._max_value)

        pygame.draw.line(screen, self._bar_colour,
                  (self._x - self._button_radius_hovered, self._y),
                  (self._x + self.get_step_in_pixels() * (self._value - self._min_value) - radius, self._y),
                  self._bar_width)
        pygame.draw.line(screen, self._bar_colour,
                  (self._x + self.get_step_in_pixels() * (self._value - self._min_value) + radius, self._y),
                  (self._x + self._width + self._button_radius_hovered, self._y), self._bar_width)
        pygame.draw.circle(screen, self._button_colour,
                    (self._x + self.get_step_in_pixels() * (self._value - self._min_value), self._y),
                    radius, 3)
        pygame.draw.circle(screen, self._button_outline_colour,
                    (self._x + self.get_step_in_pixels() * (self._value - self._min_value), self._y),
                    radius, 1)
        self.title_label.draw(screen)
        self.value_label.draw(screen)

    def events(self, e: pygame.event.Event) -> None:
        """
        Track the horizontal slider events.
        """
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == MouseStates.LMB:
                self._button_held = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == MouseStates.LMB:
                if self.is_hovering_over_button():
                    self._button_held = True
                if self.is_hovering_over() and not self._button_held:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self._value = round((mouse_x - self._x) // self.get_step_in_pixels()) + self._min_value
                    self._value = clamp(self._value, self._min_value, self._max_value)
        if e.type == pygame.MOUSEWHEEL and self.is_hovering_over():
            self._value = clamp(self._value + e.y, self._min_value, self._max_value)
        self.value_label.set_text(f"{self._value} FPS")

    def update(self, window) -> None:
        """
        Update the horizontal slider and its components.
        """
        self._width = clamp(window.width * 0.2, HorizontalSlider.MIN_WIDTH, HorizontalSlider.MAX_WIDTH)
        self.title_label.set_auto_font_size(window.width, window.height, window.max_width, window.max_height)
        self.value_label.set_auto_font_size(window.width, window.height, window.max_width, window.max_height)
        self.refresh()

    def refresh(self) -> None:
        """
        Refresh the horizontal slider and its components.
        """
        self.title_label.center_horizontally(self._x, self._width)
        self.value_label.set_x(self._x + self._width + 35)
        self.title_label.set_y(self._y - 40)
        self.value_label.set_y(self._y - 13)
        self.title_label.refresh()
        self.value_label.refresh()

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
        """
        Return whether the user's mouse cursor is hovering over the horizontal slider or not.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width
                and self._y - self._button_radius <= mouse_y <= self._y + self._bar_width + self._button_radius
                and self._enabled)

    def center_horizontally(self, parent_x: int, parent_width: int) -> Self:
        """
        Center the horizontal slider horizontally relative to the specified parent, then return the horizontal slider
        itself.
        """
        self._x = round(parent_x + parent_width / 2 - self._width / 2)
        self.refresh()
        return self

    def center_vertically(self, parent_y: int, parent_height: int) -> Self:
        """
        Center the horizontal slider vertically relative to the specified parent, then return the horizontal slider
        itself.
        """
        self._y = round(parent_y + parent_height / 2 - 2)
        self.refresh()
        return self

    def center(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int) -> Self:
        """
        Center the horizontal slider on both axes relative to the specified parent, then return the horizontal slider
        itself.
        """
        self.center_horizontally(parent_x, parent_width).center_vertically(parent_y, parent_height)
        self.refresh()
        return self

    def center_with_offset(self, parent_x: int, parent_y: int, parent_width: int, parent_height: int, x: int, y: int) -> Self:
        """
        Center the horizontal slider with center() and offset it by x and y relative to the specified parent, then
        return the horizontal slider itself.
        """
        self.center(parent_x, parent_y, parent_width, parent_height).offset(x, y)
        self.refresh()
        return self

    def get_width(self) -> int:
        """
        Return the width of the horizontal slider.
        """
        return self._width

    def get_height(self) -> int:
        """
        Return the height of the horizontal slider.
        """
        return self._height

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
