"""
Module name: pause_screen
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from game.core.game import Game
from game.gui.button import Button
from game.gui.screens.screen import Screen


class PauseScreen(Screen):
    """
    Class for creating the pause screen.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.faded_surface = None
        self.resume_button = Button(text="Resume")
        self.options_button = Button(text="Options")
        self.disconnect_button = Button(text="Disconnect")

    def translate(self) -> None:
        pass

    def draw(self) -> None:
        if not self._enabled: return
        self.game.screen.blit(self.faded_surface, (0, 0))
        self.resume_button.draw(self.game.screen)
        self.options_button.draw(self.game.screen)
        self.disconnect_button.draw(self.game.screen)

    def update_ui(self) -> None:
        if not self._enabled: return
        self.faded_surface = self.initialise_surface()
        self.resume_button.resize(self.game)
        self.options_button.resize(self.game)
        self.disconnect_button.resize(self.game)
        self.options_button.center(0, 0, self.game.width, self.game.height)
        self.disconnect_button.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            self.options_button.get_height() + 5
        )
        self.resume_button.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            -self.disconnect_button.get_height() - 5
        )
        self.resume_button.update(self.game)
        self.options_button.update(self.game)
        self.disconnect_button.update(self.game)

    def set_state(self, state: bool) -> None:
        super().set_state(state)
        self.resume_button.set_state(state)
        self.options_button.set_state(state)
        self.disconnect_button.set_state(state)
        if state: self.update_ui()
