"""
Module name: screen

This module defines the base class for all graphical user interfaces.
"""

from __future__ import annotations
from pygame import Surface
from pygame.event import Event
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING: from game.core.game import Game
from game.data.properties.screen_properties import ScreenProperties


class Screen:
    """
    Class for creating a screen.
    """

    def __init__(self, game: Game) -> None:
        self.game = game
        self._enabled = False

    def initialise_surface(self, alpha: int = ScreenProperties.ALPHA) -> Surface:
        """
        Initialise the screen's surface.
        """
        surface = Surface((self.game.width, self.game.height))
        surface.fill((0, 0, 0))
        surface.set_alpha(alpha)
        return surface

    def events(self, e: Event) -> None:
        """
        Handle the screen events.
        """
        ...

    def draw(self) -> None:
        """
        Draw the screen and its components.
        """
        ...

    def update_ui(self) -> None:
        """
        Update the screen and its components.
        """
        ...

    def translate(self) -> None:
        """
        Update the text of all text-related components to their translated equivalents.
        """
        ...

    def set_state(self, state: bool) -> Self:
        """
        Set the screen's visibility and interactivity state, then return the screen itself
        """
        self._enabled = state
        return self

    def get_state(self) -> bool:
        """
        Return the screen's visibility and interactivity state.
        """
        return self._enabled
