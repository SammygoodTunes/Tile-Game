"""
Module name: gameover_screen
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING: from game.core.game import Game
from game.gui.button import Button
from game.gui.label import Label
from game.gui.screens.screen import Screen


class GameoverScreen(Screen):
    """
    Class for creating the game-over screen.
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.faded_surface = None
        self.gameover_label = Label(text="You died.")
        self.respawn_button = Button(text="Respawn")
        self.disconnect_button = Button(text="Disconnect")

    def draw(self) -> None:
        if not self._enabled: return
        self.game.screen.blit(self.faded_surface, (0, 0))
        self.gameover_label.draw(self.game.screen)
        self.respawn_button.draw(self.game.screen)
        self.disconnect_button.draw(self.game.screen)

    def update_ui(self) -> None:
        if not self._enabled: return
        self.faded_surface = self.initialise_surface()
        self.respawn_button.resize(self.game)
        self.disconnect_button.resize(self.game)
        self.gameover_label.update(self.game)
        self.gameover_label.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            -self.respawn_button.get_height() - 25
        )
        self.respawn_button.center_with_offset(0, 0, self.game.width, self.game.height, 0, -20)
        self.disconnect_button.center_with_offset(
            0,
            0,
            self.game.width,
            self.game.height,
            0,
            self.respawn_button.get_height() - 15
        )
        self.respawn_button.update(self.game)
        self.disconnect_button.update(self.game)

    def set_state(self, state: bool) -> None:
        super().set_state(state)
        self.gameover_label.set_state(state)
        self.respawn_button.set_state(state)
        self.disconnect_button.set_state(state)
        if state: self.update_ui()
