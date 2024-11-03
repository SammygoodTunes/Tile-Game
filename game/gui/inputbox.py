"""
Module name: inputbox
"""

from __future__ import annotations
import pygame.time
from pygame import (
    mouse,
    scrap,
    draw,
    MOUSEBUTTONDOWN,
    KEYDOWN,
    K_BACKSPACE,
    K_v, Surface,
    KMOD_CTRL
)
from pygame.event import Event
from pygame.math import clamp
from string import printable, digits, ascii_letters
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING: from game.core.window import Window
from game.data.properties.gui_properties import GuiProperties
from game.data.properties.screen_properties import ScreenProperties
from game.data.states.mouse_states import MouseStates
from game.gui.label import Widget, Label
from game.gui.tooltip import Tooltip


class InputBox(Widget):
    """
    Class for creating an input box.
    """

    def __init__(self,
                 text: str = '',
                 placeholder_text: str = '',
                 tooltip_text: str = '',
                 x: int = 0,
                 y: int = 0,
                 width: int = 800,
                 height: int = 50) -> None:
        super().__init__(x, y, width, height)
        self.MIN_WIDTH = 25
        self.MIN_HEIGHT = 10
        self.validate_dimensions(width, height)
        self.MAX_WIDTH = width
        self.MAX_HEIGHT = height
        self._selected = False
        self._border_colour = (255, 255, 255)
        self._background_colour = (0, 0, 0)
        self._cursor_colour = (190, 255, 10)
        self._text_value = text
        self._text_offset = 0
        self._max_text_length = 64
        self._authorised_chars = printable[:-5]
        self._tooltip = Tooltip(text=tooltip_text)
        self._placeholder_label = Label(placeholder_text, x=5).set_font_sizes((8, 10, 12)).set_colour((225, 225, 225)).set_transparency(0.5)
        self._text_label = Label(self._text_value, x=5).set_font_sizes((8, 10, 12))
        self._timer = pygame.time.get_ticks() / 1000.0
        self._read_only = False

    def draw(self, window: Window | Surface) -> None:
        if not self._enabled:
            return
        background_surface = Surface((self._width, self._height))
        background_surface.set_alpha(ScreenProperties.ALPHA)
        draw.rect(background_surface, self._background_colour, (self._x, self._y, self._width, self._height))
        window.blit(background_surface, (self._x, self._y))
        draw.rect(window, self._border_colour, (self._x - 2, self._y - 2, self._width + 2, self._height + 2), 2)
        if self._text_value.strip():
            self._text_label.draw(window)
        elif not self._text_value.strip() and self._placeholder_label.get_width() < self._width - 10:
            self._placeholder_label.draw(window)
        if not self._selected:
            self._timer = pygame.time.get_ticks() / 1000.0
            if self.is_hovering_over() and self._can_interact:
                self._tooltip.draw(window)
            return
        if pygame.time.get_ticks() / 1000.0 - self._timer > GuiProperties.INPUTBOX_CURSORBLINK_ANIM_DURATION:
            self._timer = pygame.time.get_ticks() / 1000.0
        if pygame.time.get_ticks() / 1000.0 - self._timer <= GuiProperties.INPUTBOX_CURSORBLINK_ANIM_DURATION / 2:
            draw.rect(
                window,
                self._cursor_colour,
                (self._x + self._text_label.get_width() + 4, self._y + 8, 2, self._height - 16)
            )

    def events(self, e: Event) -> None:
        if self._read_only or not self._can_interact:
            return
        if e.type == MOUSEBUTTONDOWN:
            if e.button == MouseStates.LMB:
                self._selected = self.is_hovering_over()
                self._timer = pygame.time.get_ticks() / 1000.0
        if e.type == KEYDOWN and self._selected:
            if e.key == K_BACKSPACE:
                if e.mod & KMOD_CTRL:
                    index = self._text_value.rfind(' ')
                    new = self._text_value[:index]
                    length = len(self._text_value) - len(new)
                    self._text_value = new if index != -1 else ''
                else:
                    self._text_value = self._text_value[:-1]
                    length = 1
                if self._text_offset > 0:
                    self._text_offset -= length
            elif e.key == K_v and e.mod & KMOD_CTRL:
                self._text_value += self.clean_text(
                    scrap.get("text/plain;charset=utf-8").decode()
                )[:self._max_text_length - len(self._text_value)]
            elif e.unicode in self._authorised_chars and e.unicode.isascii():
                self._text_value += e.unicode if len(self._text_value) < self._max_text_length else ''
            self.scroll_text()
            self._text_label.set_text(self._text_value[self._text_offset:])

    def update(self, window: Window) -> None:
        if not self._enabled:
            return
        self._width = int(clamp(window.width * 0.4, self.MIN_WIDTH, self.MAX_WIDTH))
        self._height = int(clamp(window.height * 0.1, self.MIN_HEIGHT, self.MAX_HEIGHT))
        self.scroll_text()
        self._text_label.update(window)
        self._text_label.set_text(self._text_value[self._text_offset:])
        self._tooltip.update(window)
        self._placeholder_label.update(window)
        self._placeholder_label.center_vertically(self._y - 2, self._height)
        self._placeholder_label.set_x(self._x + 5)
        self._text_label.center_vertically(self._y - 2, self._height)
        self._text_label.set_x(self._x + 5)

    def scroll_text(self) -> None:
        """
        Internal method for calculating how and when to scroll text when going beyond the input box.
        I am aware of how awful it is. Why? because O(n).
        What does that mean? the larger the text, the slower it gets! Very bad!
        Might not be that noticeable for small strings, but still...
        TODO: Make it better, fool.
        """
        diff = self._text_label.font.size(self._text_value)[0] - (self._width - 10)
        value = 0
        if diff > 0 or (diff < 0 < self._text_offset):
            for i, _ in enumerate(self._text_value):
                value += self._text_label.font.size(self._text_value[i])[0]
                if value >= diff + 10:
                    self._text_offset = i
                    break

    def clean_text(self, text: str) -> str:
        """
        Clean the text of any unauthorised characters.
        """
        for char in text:
            if char in self._authorised_chars:
                continue
            text = text.replace(char, '')
        return text

    def authorise_only_ascii(self) -> Self:
        """
        Authorise only ASCII characters in the input box, then return the input box itself.
        """
        self._authorised_chars = printable[:-5]
        return self

    def authorise_only_numeric(self) -> Self:
        """
        Authorise only numerical values (0-9) in the input box, then return the input box itself.
        """
        self._authorised_chars = digits
        return self

    def authorise_only_alnum(self) -> Self:
        """
        Authorise only alphanumerical values (a-zA-Z0-9), then return the input box itself.
        """
        self._authorised_chars = ascii_letters + digits
        return self

    def authorise_only_alnumlines(self) -> Self:
        """
        Authorise only alphanumerical values (a-zA-Z0-9-_), then return the input box itself.
        This includes dashes (hyphens) and underscores.
        """
        self._authorised_chars = ascii_letters + digits + '-_'
        return self

    def authorise_only_alnumdot(self) -> Self:
        """
        Authorise only alphanumerical values (a-zA-Z0-9.), then return the input box itself.
        This includes the dot (period/full stop) character.
        """
        self._authorised_chars = ascii_letters + digits + '.'
        return self

    def is_hovering_over(self) -> bool:
        mouse_x, mouse_y = mouse.get_pos()
        return (self._x <= mouse_x <= self._x + self._width and
                self._y <= mouse_y <= self._y + self._height and self._enabled)

    def set_selected(self, state) -> Self:
        """
        Set the selected state of the input box, then return the input box itself.
        """
        self._selected = state
        return self

    def is_selected(self) -> bool:
        """
        Return whether the input box is selected or not.
        """
        return self._selected

    def set_border_colour(self, border_colour: tuple[int, int, int]) -> Self:
        """
        Set the border colour of the input box, then return the input box itself.
        """
        self._border_colour = border_colour
        return self

    def get_border_colour(self) -> tuple[int, int, int]:
        """
        Return the border colour of the input box.
        """
        return self._border_colour

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

    def set_cursor_colour(self, cursor_colour: tuple[int, int, int]) -> Self:
        """
        Set the cursor colour of the input box, then return the input box itself.
        """
        self._cursor_colour = cursor_colour
        return self

    def get_cursor_colour(self) -> tuple[int, int, int]:
        """
        Return the cursor colour of the input box.
        """
        return self._cursor_colour

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

    def set_max_text_length(self, max_text_length: int) -> Self:
        """
        Set the input box's max text length, then return the input box itself.
        """
        self._max_text_length = max_text_length
        return self

    def get_max_text_length(self) -> int:
        """
        Return the input box's max text length.
        """
        return self._max_text_length

    def set_text_colour(self, text_colour: tuple[int, int, int]) -> Self:
        """
        Set the text colour, then return the input box itself.
        """
        self._text_label.set_colour(text_colour)
        return self

    def set_placeholder_text_colour(self, placeholder_text_colour: tuple[int, int, int]) -> Self:
        """
        Set the placeholder text colour, then return the input box itself.
        """
        self._placeholder_label.set_colour(placeholder_text_colour)
        return self

    def set_tooltip_text(self, tooltip_text: str) -> Self:
        """
        Set the input box's tooltip text, then return the input box itself.
        """
        self._tooltip.set_text(tooltip_text)
        return self

    def set_read_only(self, state: bool) -> Self:
        """
        Set the input box's read-only state, then return the input box itself.
        """
        self._read_only = state
        return self

    def get_read_only(self) -> bool:
        """
        Return the input box's read-only state.
        """
        return self._read_only

    def set_interact(self, state: bool) -> Self:
        super().set_interact(state)
        if not state: self._selected = state
        return self
